import json
from tkinter import Image
import qrcode
import base64
from io import BytesIO
import logging
from api.serializers import *
from PIL import Image
from rest_framework import status
from rest_framework.views import APIView
from database.database_management import *
from rest_framework.response import Response
from database.connection import dowellconnection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt



@method_decorator(csrf_exempt, name='dispatch')
class codeqr(APIView):
    def post(self, request):
        link = request.data.get("link")
        product_name = request.data.get("product_name")
        logo = request.FILES.get('logo')
        create_by = request.data.get("create_by")
        company_id = request.data.get("company_id")

        # logo_image = Image.open("image/logo.png")
        logo_image = Image.open(BytesIO(base64.b64decode(logo)))
        logo_image = logo_image.convert("RGBA")

        print("Logo image size:", logo_image.size)

        # Create the QR code image
        qr_code = qrcode.QRCode(version=1, 
                                error_correction=qrcode.constants.ERROR_CORRECT_L, 
                                box_size=10, border=4)
        qr_code.add_data(link)
        qr_code.make(fit=True)
        img_qr = qr_code.make_image(fill_color="black", back_color="white")
        print("QR code size:", img_qr.size)

        # Calculate the position to place the logo
        logo_size = min(img_qr.size[0], img_qr.size[1]) * 25 // 100 # Change this value to adjust the size of the logo
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

        # Encode the QR code image to base64
        buffer = BytesIO()
        img_qr.save(buffer, 'PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        field = {
            "link": link,
            "logo": logo_base64,
            "create_by" : create_by,
            "company_id": company_id,
            "product_name":  product_name,
            "qrcode": img_base64
        }
        update_field = {
            "status":"nothing to update"
        }

        

        serializer = DoWellQrCodeSerializer(data=field)
        if serializer.is_valid():
            response = dowellconnection(*qrcode_management,"insert",field, update_field)
            return Response({"Response":response,"qrcode":img_base64}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# generate_image = qrcode.make("Youtube")
# generate_image.save('image1.png')


# Binary data is a type of digital data that is represented using a binary system of 0s and 1s. In computing,
# binary data typically refers to any data that is not text-based, such as images, audio files, video files, and executable programs.

