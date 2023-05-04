import io
import json
# from tkinter import Image
import qrcode
import base64
from io import BytesIO
import logging
import re
from api.serializers import *

from PIL import Image, ImageDraw, ImageOps, ImageFilter
from rest_framework import status
from rest_framework.views import APIView
from api.utils import change_image_color_, resize_image
from database.database_management import *
from rest_framework.response import Response
from database.connection import dowellconnection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt



def is_valid_hex_color(color):
    """
    Checks if the given string is a valid hex color code.
    """
    if not isinstance(color, str):
        return False
    if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
        return False
    return True


@method_decorator(csrf_exempt, name='dispatch')
class codeqr(APIView):
    serializer_class = DoWellQrCodeSerializer

    def post(self, request):
        company_id = request.data.get("company_id")
        link = request.data.get("link")
        logo = request.FILES.get('logo')
        logo_size = request.data.get("logo_size")
        qrcode_color = request.data.get('qrcode_color')
        # product_name = request.data.get("product_name")
        # create_by = request.data.get("create_by")
    
        # logo_image = Image.open("logo.png")

        # set default logo size if no logo_size is found
        if logo_size:
            logo_size = int(logo_size)
        else:
            logo_size = 20
        if logo and logo.size > 0:
            logo_contents = logo.read()
            logo_image = Image.open(io.BytesIO(logo_contents))
            
            # Resize the logo to the desired size
            logo_image = logo_image.resize((logo_size, logo_size), resample=Image.LANCZOS)
            
        else:
            logo_image = None

        # Create the QR code image
        qr_code = qrcode.QRCode(version=1, 
                                error_correction=qrcode.constants.ERROR_CORRECT_Q, 
                                box_size=10, border=4)
        
        if link:
            qr_code.add_data(link)
        else:
            pass
        qr_code.make(fit=True)
        img_qr = qr_code.make_image(fill_color=qrcode_color, back_color="white")

        if logo_image:
            # Calculate the position to place the logo
            qrcode_logoSize = min(img_qr.size[0], img_qr.size[1]) * 25 // 100 # Change this value to adjust the size of the logo
            logo_x = (img_qr.size[0] - qrcode_logoSize) // 2
            logo_y = (img_qr.size[1] - qrcode_logoSize) // 2

            # Resize the logo to the desired size
            logo_image = logo_image.resize((qrcode_logoSize, qrcode_logoSize), resample=Image.LANCZOS)

            # Paste the logo on the QR code image
            img_qr.paste(logo_image, (logo_x, logo_y))

            # Encode the logo image to base64
            buffer = BytesIO()
            logo_image.save(buffer, format="PNG")
            logo_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        else:
            logo_base64 = None

        # Encode the QR code image to base64
        buffer = BytesIO()
        img_qr.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        logoSize = logo_size
        field = {
            "logo": logo_base64,
            "qrcode": img_base64,
            "logo_size": logoSize,
            "company_id": company_id,
            "qrcode_color": qrcode_color,
        }
        update_field = {
            "status":"nothing to update"
        }

        # python qrcode
        serializer = DoWellQrCodeSerializer(data=field)
        # serializer = DoWellQrCodeSerializer(data=field)
        if serializer.is_valid():
            serializer.save(is_active=False)
            # response = dowellconnection(*qrcode_management,"insert",field, update_field)
            # return Response({"Response":serializer.data ,"logo":logo_base64,"qrcode":img_base64}, status=status.HTTP_201_CREATED)
            return Response({"Response":serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        company_id = request.GET.get('company_id')

        if company_id:
            try:
                qrCode = QrCode.objects.get(company_id=company_id)
                serializer = self.serializer_class(qrCode, many=False)
                return Response({"data": serializer.data})
            except qrCode.DoesNotExist:
                return Response({"error": "Not Found"})
        else:
            return Response({"error": "Please provide either company_id or product_name"}, status=status.HTTP_400_BAD_REQUEST)

        # update_field = {"status": "nothing to update"}
        # response = dowellconnection(*qrcode_management, "fetch", field, update_field)
        # return Response({"Response": json.loads(response)}, status=status.HTTP_200_OK)




@method_decorator(csrf_exempt, name='dispatch')
class codeqrupdate(APIView):
    def put(self, request, id):

        company_id = request.data.get("company_id")
        link = request.data.get("link")
        logo = request.FILES.get('logo')
        logo_size = int(request.data.get("logo_size"))
        qrcode_color = request.data.get('qrcode_color', "#000000")

        # Validate logo size
        try:
            logo_size = int(logo_size)
            if logo_size <= 0:
                raise ValueError("Logo size must be a positive integer.")
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
        if not is_valid_hex_color(qrcode_color):
            return Response({"error": "Invalid logo color. Must be a valid hex color code."}, status=status.HTTP_400_BAD_REQUEST)
        
        if logo and logo.size > 0:
            logo_contents = logo.read()
            logo_image = Image.open(io.BytesIO(logo_contents))
            
            logo_image = logo_image.resize((logo_size, logo_size), resample=Image.LANCZOS)            
        else:
            logo_image = None

        # Create the QR code image
        qr_code = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=10, border=4)
        qr_code.add_data(link)
        qr_code.make(fit=True)
        img_qr = qr_code.make_image(fill_color=qrcode_color, back_color="white")


        if logo_image:
            # Calculate the position to place the logo
            logo_size = min(img_qr.size[0], img_qr.size[1]) * 25 // 100  # Change this value to adjust the size of the logo
            logo_x = (img_qr.size[0] - logo_size) // 2
            logo_y = (img_qr.size[1] - logo_size) // 2

            # Resize the logo to the desired size
            logo_image = logo_image.resize((logo_size, logo_size), resample=Image.LANCZOS)

            # Paste the logo on the QR code image
            img_qr.paste(logo_image, (logo_x, logo_y))

            # Encode the logo image to base64
            buffer = BytesIO()
            logo_image.save(buffer, format="PNG")
            logo_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        else:
            logo_base64 = None

        # Encode the QR code image to base64
        buffer = BytesIO()
        img_qr.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        logoSize = int(request.data.get("logo_size"))
        field = {
            "link": link,
            "logo": logo_base64,
            "qrcode": img_base64,
            "logo_size": logoSize,
            "company_id": company_id,
            "qrcode_color": qrcode_color,
            "is_active": True
        }
       
        update_field = {
            "status":"nothing to update"
        }

        try:
            code = QrCode.objects.get(company_id = id)
            serializer = DoWellQrCodeSerializer(code, data=field, partial=True)
            if serializer.is_valid():
                serializer.save()
                # response = dowellconnection(*qrcode_management,"insert",field, update_field)
                return Response({"Response":serializer.data}, status=status.HTTP_201_CREATED)
        except :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

           

 
      

