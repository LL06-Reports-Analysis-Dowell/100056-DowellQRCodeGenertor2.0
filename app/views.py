
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
    create_uuid, is_valid_hex_color, create_qrcode,
    dowellconnection, update_cloudinary_image, 
    upload_image_to_cloudinary
)
from .constant import *

from .serializers import DoWellQrCodeSerializer, DoWellUpdateQrCodeSerializer


# In the below code, the codeqr class now accepts a list of QR code data in the request body.
#  Each item in the list represents a set of data for generating a QR code. The code iterates over each item,
#  processes it, and collects the results in a list. 
# Finally, the results are returned as a response, containing information about the success or failure of each QR code generation.
# This updated code merges the functionality of both classes into a single CodeQR class. 
# It includes the necessary decorators, combines the logic for generating multiple QR codes with default values,
#  and incorporates the existing code logic for each generated QR code. The response includes the list of generated QR code data (qr_codes) 
# and the results of the existing code logic (results).


@method_decorator(csrf_exempt, name='dispatch')
class serverStatus(APIView):
    def get(self, request):
        return Response({"info":"QrCode Backend servies running fine."}, status= status.HTTP_200_OK)
    


class codeqr(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        data = request.data
        qr_code_no = data.get("qr-code_no")  # Get the number of QR codes

        qr_codes = []
        results = []

        for i in range(qr_code_no):
            # Generate the QR code with default values
            qr_code_data = {
                "company_id": "Default Company ID",
                "link": "https://example.com",
                "logo_size": 20,
                "qrcode_color": "#000000",
                "product_name": f"Product {i+1}",
                "created_by": "Default User",
                "description": "Default Description",
                "is_active": False
            }

            # Perform the existing code logic for each QR code
            item = qr_code_data
            # get post data
            company_id = item.get("company_id")
            link = item.get("link")
            logo = item.FILES.get('logo')
            logo_size = int(item.get("logo_size", "20"))
            qrcode_color = item.get('qrcode_color', "#000000")
            product_name = item.get("product_name")
            created_by = item.get("created_by")
            description = item.get("description")
            is_active = item.get("is_active", False)

            # Validate logo size
            try:
                if logo_size <= 0:
                    raise ValueError("Logo size must be a positive integer.")
            except ValueError as e:
                results.append({"error": str(e)})
                continue

            if not is_valid_hex_color(qrcode_color):
                results.append({"error": "Invalid logo color. Must be a valid hex color code."})
                continue

            if logo:
                logo_file = logo.read()
                logo_url = upload_image_to_cloudinary(logo_file)
            else:
                logo_url = None

            # Create the QR code image and center logo if passed
            img_qr = create_qrcode(link, qrcode_color, logo)

            # Upload qrcode_image to cloudinary
            qr_code_url = upload_image_to_cloudinary(img_qr)

            field = {
                "qrcode_id": create_uuid(),
                "qrcode_image_url": qr_code_url,
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
                "status": "nothing to update"
            }

            serializer = DoWellQrCodeSerializer(data=field)
            if serializer.is_valid():
                try:
                    insertion_thread = threading.Thread(target=self.mongodb_worker, args=(field, update_field))
                    insertion_thread.start()
                    results.append({"response": field})
                except:
                    results.append({"error": "An error occurred while starting the insertion thread"})
            else:
                results.append({"error": serializer.errors})

            qr_codes.append(qr_code_data)

        # Return the list of QR code data as the response
        response_data = {
            "results": results,
            "qr_codes": qr_codes
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

     
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
            logo_url = upload_image_to_cloudinary(logo_file)
        elif logo_url and logo:
            logo_url = update_cloudinary_image(logo_url, logo)
        else:
            pass

        # Create the QR code image
        img_qr = create_qrcode(link, qrcode_color, logo)

        # update qrcode and logo image in cloudinary
        qrcode_image_url = update_cloudinary_image(qrcode_image_url, img_qr)

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

    
      


