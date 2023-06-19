
import json
import base64
from io import BytesIO
import threading
from PIL import Image
import io
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .helper import (
    create_uuid, generate_file_name, is_valid_hex_color, create_qrcode,
    dowellconnection, qrcode_type_defination, update_cloudinary_image, 
    upload_image_to_interserver
)
from .constant import *

from .serializers import DoWellUpdateQrCodeSerializer

@method_decorator(csrf_exempt, name='dispatch')
class serverStatus(APIView):
    def get(self, request):
        return Response({"info":"QrCode Backend servies running fine."}, status= status.HTTP_200_OK)
    


class codeqr(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        company_id = request.data.get("company_id")
        qrcode_type = request.data.get("qrcode_type")
        # link = request.data.get("link")
        logo = request.FILES.get('logo')  
        logo_size = int(request.data.get("logo_size", "20"))
        qrcode_color = request.data.get('qrcode_color', "#000000")

        created_by = request.data.get("created_by")
        description = request.data.get("description")
        is_active = request.data.get("is_active", False)
        quantity = int(request.data.get("quantity"))


        try:
            if logo_size <= 0:
                raise ValueError("Logo size must be a positive integer.")
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not is_valid_hex_color(qrcode_color):
            return Response({"error": "Invalid logo color. Must be a valid hex color code."}, status=status.HTTP_400_BAD_REQUEST)
                
        
        if logo:
            logo_file = logo.read() # This line affects the create_qrcode function below(converts InMemoryUploadedFile to bytes)     
        else:
            pass

        # if quantity:
        for _ in range(quantity):
            logo_url = None

            if logo:
                logo_url = upload_image_to_interserver(logo_file, logo.name)
            else:
                logo_url = None

            field = {
                "qrcode_id": create_uuid(),
                # "qrcode_image_url": qr_code_url,
                # "logo_url": logo_url,
                "logo_size": logo_size,
                "qrcode_color": qrcode_color,
                # "link": link,
                "company_id": company_id,
                "created_by": created_by,
                "description": description,
                "is_active": is_active,
                "qrcode_type": qrcode_type,
                
            }

            update_field = {
                "status":"nothing to update"
            }

            # This function checks qrcode_type field and assign them appropriate properties
            serializer, field = qrcode_type_defination(qrcode_type, request, qrcode_color, logo, field, logo_url)

            if serializer.is_valid():
                try:
                    insertion_thread = threading.Thread(target=self.mongodb_worker, args=(field, update_field))
                    insertion_thread.start()
                    # return Response({"response": field}, status=status.HTTP_201_CREATED)
                except:
                    return Response({"error": "An error occurred while starting the insertion thread"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response({"response": f"{quantity} QR codes created successfully."}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

     
    def mongodb_worker(self, field, update_field):
        dowellconnection(*qrcode_management,"insert", field, update_field)
    
    
    def get(self, request):
        try:
            company_id = request.GET.get('company_id')
            product_name = request.GET.get('product_name')
        except:
            pass

        if company_id:
            field = {"company_id": company_id}
        elif product_name:
            field = {"product_name": product_name}
        else:
            # I if no params are passed get all qrcodes
            response = dowellconnection(*qrcode_management, "fetch", {}, {})
            return Response({"response": json.loads(response)}, status=status.HTTP_200_OK)
        
        # update_field = {"status": "nothing to update"}
        response = dowellconnection(*qrcode_management, "fetch", field, {})
        return Response({"response": json.loads(response)}, status=status.HTTP_200_OK)




@method_decorator(csrf_exempt, name='dispatch')
class codeqrupdate(APIView):

    def get_object(self, request, id):
        field = {"qrcode_id": id}  
        res = dowellconnection(*qrcode_management, "fetch", field, {})
        response = json.loads(res)
        if response["isSuccess"]:
            return response["data"][0]
        
    
    def get(self, request, id):
        field = {"qrcode_id": id}  
        res = dowellconnection(*qrcode_management, "fetch", field, {})
        response = json.loads(res)

        # Check if the fetch was successful
        if response["isSuccess"]:
            return Response({"response": response["data"]}, status=status.HTTP_200_OK)
        else:
            return Response({"error": response["error"]}, status=status.HTTP_400_BAD_REQUEST)
   
    
    def put(self, request, id):

        # get cloudinary qrcode image in order to update it
        logo_url = ""
        
        try:
            qrcode_ = self.get_object(request, id)
            qrcode_image_url = qrcode_["qrcode_image_url"]
            logo_url = qrcode_["logo_url"]
        except: 
            pass

        company_id = request.data.get("company_id")
        link = request.data.get("link")
        logo = request.FILES.get('logo')
        logo_size = int(request.data.get("logo_size", "20"))
        qrcode_color = request.data.get('qrcode_color', "#000000")
        product_name = request.data.get("product_name")
        created_by = request.data.get("created_by")
        description = request.data.get("description")
        is_active = request.data.get("is_active", True)

        # Validate logo size
        try:
            if logo_size <= 0:
                raise ValueError("Logo size must be a positive integer.")
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not is_valid_hex_color(qrcode_color):
            return Response({"error": "Invalid logo color. Must be a valid hex color code."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not logo and not logo_url:
            logo_url = None
        elif not logo_url and logo:
            logo_file = logo.read()
            logo_url = upload_image_to_interserver(logo_file, logo.name)
        elif logo_url and logo:
            # logo_url = update_cloudinary_image(logo_url, logo)
            logo_url = upload_image_to_interserver(logo, logo.name)
        else:
            pass

        # Create the QR code image
        img_qr = create_qrcode(link, qrcode_color, logo)

        # update qrcode and logo image in cloudinary
        file_name = generate_file_name()
        qrcode_image_url = upload_image_to_interserver(img_qr, file_name)
        # qrcode_image_url = update_cloudinary_image(qrcode_image_url, img_qr)

        logoSize = logo_size

        field = {
            "qrcode_id": id
        }
       
        update_field = {
            "qrcode_image_url": qrcode_image_url,
            "logo_url": logo_url,
            "logo_size": logoSize,
            "qrcode_color": qrcode_color,
            "link": link,
            "company_id": company_id,
            "product_name": product_name,
            "created_by": created_by,
            "description": description,
            "is_active": is_active,
        }

        serializer = DoWellUpdateQrCodeSerializer(data=update_field)
        if serializer.is_valid():
            res = dowellconnection(*qrcode_management,"update",field, update_field)
            response = json.loads(res)

            # Check if the update was successful
            if response["isSuccess"]:
                return Response({"response": update_field}, status=status.HTTP_200_OK)
            else:
                return Response({"error": response["error"]}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
      











