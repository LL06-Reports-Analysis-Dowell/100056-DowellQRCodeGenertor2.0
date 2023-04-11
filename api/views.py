import json
from tkinter import Image
import qrcode
import base64
from io import BytesIO
from api.serializers import *
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
        logo = request.data.get('logo')
        create_by = request.data.get("create_by")
        company_id = request.data.get("company_id")


        # logo_data = decode_base64(logo)
        # logo_image = Image.open
        qr_code = qrcode.QRCode(version=1, 
                            error_correction=qrcode.constants.ERROR_CORRECT_L, 
                            box_size=10, border=4)
        qr_code.add_data(link)
        qr_code.make(fit=True)
        img_qr = qr_code.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img_qr.save(buffer, 'PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')


        field = {
            "link": link,
            "logo": logo,
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

