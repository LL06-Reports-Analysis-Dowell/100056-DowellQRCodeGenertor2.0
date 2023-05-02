import io
import json
# from tkinter import Image
import qrcode
import base64
from io import BytesIO
import logging
import re
from api.serializers import *

import numpy as np
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

def change_image_color(image, color_from, color_to):
    """
    Changes the color of the given image from color_from to color_to.
    """
    if not is_valid_hex_color(color_from):
        raise ValueError("Invalid hex color code for color_from.")
    if not is_valid_hex_color(color_to):
        raise ValueError("Invalid hex color code for color_to.")

    # Convert color codes to RGB tuples
    rgb_from = tuple(int(color_from[i:i+2], 16) for i in (1, 3, 5))
    rgb_to = tuple(int(color_to[i:i+2], 16) for i in (1, 3, 5))

    # Replace the color in the image
    data = np.array(image)
    r, g, b, a = np.rollaxis(data, axis=-1)
    mask = (r == rgb_from[0]) & (g == rgb_from[1]) & (b == rgb_from[2])
    data[..., :-1][mask] = rgb_to
    return Image.fromarray(data)
@method_decorator(csrf_exempt, name='dispatch')
class codeqr(APIView):


    def post(self, request):
        link = request.data.get("link")
        print("This the link", link)
        product_name = request.data.get("product_name")
        logo = request.FILES.get('logo')
        print("Fileimageeee:", logo)
        create_by = request.data.get("create_by")
        company_id = request.data.get("company_id")

        logo_color = request.data.get("logo_color")
        logo_size = 100 # Set default logo size
        
        # logo_image = Image.open("logo.png")

        if logo and logo.size > 0:
            logo_contents = logo.read()
            logo_image = Image.open(io.BytesIO(logo_contents))
            print("Logo image size:", logo_image.size)
            

            # Resize the logo to the desired size
            logo_image = logo_image.resize((logo_size, logo_size), resample=Image.LANCZOS)
            
        else:
            logo_image = None

        # Create the QR code image
        qr_code = qrcode.QRCode(version=1, 
                                error_correction=qrcode.constants.ERROR_CORRECT_Q, 
                                box_size=10, border=4)
        qr_code.add_data(link)
        print("Haiyaaaa", link)
        qr_code.make(fit=True)
        img_qr = qr_code.make_image(fill_color="black", back_color="white")
        print("QR code size:", img_qr.size)

        if logo_image:
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
            print(logo_base64)
        else:
            logo_base64 = None

        # Encode the QR code image to base64
        buffer = BytesIO()
        img_qr.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        # print(img_base64)
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
# python qrcode


        serializer = DoWellQrCodeSerializer(data=field)
        if serializer.is_valid():
            response = dowellconnection(*qrcode_management,"insert",field, update_field)
            return Response({"Response":response,"logo":logo_base64,"qrcode":img_base64}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        company_id = request.GET.get('company_id')
        product_name = request.GET.get('product_name')

        if company_id:
            field = {"company_id": company_id}
        elif product_name:
            field = {"product_name": product_name}
        else:
            return Response({"error": "Please provide either company_id or product_name"}, status=status.HTTP_400_BAD_REQUEST)

        update_field = {"status": "nothing to update"}

        response = dowellconnection(*qrcode_management, "fetch", field, update_field)
        return Response({"Response": json.loads(response)}, status=status.HTTP_200_OK)

# generate_image = qrcode.make("Youtube")
# generate_image.save('image1.png')


@method_decorator(csrf_exempt, name='dispatch')
class codeqrupdate(APIView):
    def post(self, request):
        link = request.data.get("link")
        product_name = request.data.get("product_name")
        logo = request.FILES.get('logo')
        create_by = request.data.get("create_by")
        company_id = request.data.get("company_id")
        logo_size = request.data.get("logo_size", 100)  # Get logo size from request data or set default
        logo_color = request.data.get("logo_color", "#000000")  # Get logo color from request data or set default
        qrcode_color = request.data.get("qrcode_color", "black")

        print("This is the logo color", logo_color)
        print("This is the logo", logo)
        # Validate logo size
        
        try:
            logo_size = int(logo_size)
            if logo_size <= 0:
                raise ValueError("Logo size must be a positive integer.")
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Validate logo color
        if not is_valid_hex_color(logo_color):
            return Response({"error": "Invalid logo color. Must be a valid hex color code."}, status=status.HTTP_400_BAD_REQUEST)
        
        if logo and logo.size > 0:
            logo_contents = logo.read()
            logo_image = Image.open(io.BytesIO(logo_contents))
            print("Logo image size:", logo_image.size)
            
            # Resize the logo to the desired size and change color
            logo_image = logo_image.resize((logo_size, logo_size), resample=Image.LANCZOS)
            print("logo_size after1", logo_image.size)
            change_image_color_(logo, logo_color)
            
        else:
            logo_image = None

        # Create the QR code image
        qr_code = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=10, border=4)
        qr_code.add_data(link)
        qr_code.make(fit=True)
        img_qr = qr_code.make_image(fill_color=qrcode_color, back_color="white")
        print("QR code size:", img_qr.size)

        if logo_image:
            # Calculate the position to place the logo
            logo_size = min(img_qr.size[0], img_qr.size[1]) * 25 // 100  # Change this value to adjust the size of the logo
            logo_x = (img_qr.size[0] - logo_size) // 2
            logo_y = (img_qr.size[1] - logo_size) // 2

            # Resize the logo to the desired size
            logo_image = logo_image.resize((logo_size, logo_size), resample=Image.LANCZOS)
            print("logo_size after2", logo_image.size)

            # Paste the logo on the QR code image
            img_qr.paste(logo_image, (logo_x, logo_y))

            # Change logo color
            # if logo_color != "black":
            #     img_qr = change_image_color(img_qr, "black", logo_color)

            # Encode the logo image to base64
            buffer = BytesIO()
            logo_image.save(buffer, format="PNG")
            logo_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            print(logo_base64)
        else:
            logo_base64 = None

        # Encode the QR code image to base64
        buffer = BytesIO()
        img_qr.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        field = {
            "link": link,
            "logo": logo_base64,
            "create_by" : create_by,
            "company_id": company_id,
            "product_name":  product_name,
            "logo_size": logo_size,
            "logo_color":logo_color,
            "qrcode_color": qrcode_color,
            "qrcode": img_base64
        }
        update_field = {
            "status":"nothing to update"
        }



        serializer = DoWellQrCodeSerializer(data=field)
        if serializer.is_valid():
            # response = dowellconnection(*qrcode_management,"insert",field, update_field)
            return Response({"Response":field,"logo":logo_base64,"qrcode":img_base64}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           



# Binary data is a type of digital data that is represented using a binary system of 0s and 1s. In computing,
# binary data typically refers to any data that is not text-based, such as images, audio files, video files, and executable programs.

# @method_decorator(csrf_exempt, name='dispatch')
# class fetchdata(APIView):

#     def get(self, request , company_id):
#         field = {
#            "company_id": company_id 
#         }
#         update_field = {
#             "status":"nothing to update"
#         }

#         response = dowellconnection(*qrcode_management,"fetch",field, update_field)
#         return Response({"Response":json.loads(response)}, status=status.HTTP_201_CREATED)
    



# @method_decorator(csrf_exempt, name='dispatch')
# class getdata(APIView):

#     def get(self, request , product_name):
#         field = {
#            "product_name":  product_name
#         }
#         update_field = {
#             "status":"nothing to update"
#         }

#         response = dowellconnection(*qrcode_management,"fetch",field, update_field)
#         return Response({"Response":json.loads(response)}, status=status.HTTP_201_CREATED)