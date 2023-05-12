
import json
import base64
from io import BytesIO
import threading

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .helper import create_uuid, get_base64_image_in_bytes, is_valid_hex_color, create_qrcode, logo_position, resize_logo, dowellconnection, update_cloudinary_image, upload_image_to_cloudinary
from .constant import *

from .serializers import DoWellQrCodeSerializer, DoWellUpdateQrCodeSerializer



@method_decorator(csrf_exempt, name='dispatch')
class serverStatus(APIView):
    def get(self, request):
        return Response({"info":"QrCode Backend servies running fine."}, status= status.HTTP_200_OK)
    


@method_decorator(csrf_exempt, name='dispatch')
class codeqr(APIView):
    def post(self, request):
        # get post data
        company_id = request.data.get("company_id")
        link = request.data.get("link")
        logo = request.FILES.get('logo')
        logo_size = int(request.data.get("logo_size", "20"))
        qrcode_color = request.data.get('qrcode_color', "#000000")
        product_name = request.data.get("product_name")
        created_by = request.data.get("created_by")
        description = request.data.get("description")
        is_active = request.data.get("is_active", False)

        # Validate logo size
        try:
            if logo_size <= 0:
                raise ValueError("Logo size must be a positive integer.")
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not is_valid_hex_color(qrcode_color):
            return Response({"error": "Invalid logo color. Must be a valid hex color code."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the QR code image
        img_qr = create_qrcode(link, qrcode_color)

        # resize logo
        logo_image = resize_logo(logo, logo_size)

        # center logo in the qrcode
        logo_base64 = logo_position(logo_image, img_qr)

        # Encode the QR code image to base64 and position logo at te center of the qrcode
        buffer = BytesIO()
        img_qr.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        #upload image to cloudinary
        image = upload_image_to_cloudinary(img_base64)

        if logo:
            logo_url = upload_image_to_cloudinary(logo_base64)
        else:
            logo_url = None

        field = {
            "qrcode_id": create_uuid(),
            "qrcode_image_url": image,
            "logo_url": logo_url,
            "logo_size": logo_size,
            "qrcode_color": qrcode_color,
            "link": link,
            "company_id": company_id,
            "product_name": product_name,
            "created_by": created_by,
            "description": description,
            "is_active": is_active,
        }

        update_field = {
            "status":"nothing to update"
        }
        
        serializer = DoWellQrCodeSerializer(data=field)
        if serializer.is_valid():
            try:
                insertion_thread = threading.Thread(target=self.mongodb_worker, args=(field, update_field))
                insertion_thread.start()
                return Response({"response": field}, status=status.HTTP_201_CREATED)
            except:
                return Response({"error": "An error occurred while starting the insertion thread"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
        
        # resize logo
        logo_image = resize_logo(logo, logo_size)
        
        # Create the QR code image
        img_qr = create_qrcode(link, qrcode_color)

        # center logo in the qrcode
        logo_base64 = logo_position(logo_image, img_qr)

        # Encode the QR code image to base64
        buffer = BytesIO()
        img_qr.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # decode base64_image to bytes(required by cloudinary)
        qrcode_img = get_base64_image_in_bytes(img_base64)
        logo_image = get_base64_image_in_bytes(logo_base64)

        # update qrcode and logo image in cloudinary
        qrcode_image_url = update_cloudinary_image(qrcode_image_url, qrcode_img)

        # upload logo image to cloudinary
        if not logo_url:
            logo_url = upload_image_to_cloudinary(logo_base64)
        else:
            logo_url = update_cloudinary_image(logo_url, logo_image)

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

    
      


