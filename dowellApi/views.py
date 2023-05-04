import io
import json
# from tkinter import Image
import qrcode
import base64
from io import BytesIO
import logging
import re
from localApi.serializers import *

from PIL import Image, ImageDraw, ImageOps, ImageFilter
from rest_framework import status
from rest_framework.views import APIView
from localApi.utils import is_valid_hex_color, create_qrcode, logo_position, resize_logo
from database.database_management import *
from rest_framework.response import Response
from database.connection import dowellconnection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .serializers import DoWellQrCodeSerializer, DoWellUpdateQrCodeSerializer
# create post put



@method_decorator(csrf_exempt, name='dispatch')
class codeqr(APIView):
    serializer_class = DoWellQrCodeSerializer

    def post(self, request):
        company_id = request.data.get("company_id")
        link = request.data.get("link")
        logo = request.FILES.get('logo')
        logo_size = request.data.get("logo_size")
        qrcode_color = request.data.get('qrcode_color')
        product_name = request.data.get("product_name")
        created_by = request.data.get("created_by")
        is_active = request.data.get("is_active", False)


        # set default logo size if no logo_size is found
        logo_image = resize_logo(logo, logo_size)

        # Create the QR code image
        img_qr = create_qrcode(link, qrcode_color)
       
        # Encode the QR code image to base64 and position logo at te center of the qrcode

        logo_base64 = logo_position(logo_image, img_qr)
        buffer = BytesIO()
        img_qr.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        logoSize = logo_size
        field = {
            "logo": logo_base64,
            "link": link,
            "qrcode": img_base64,
            "logo_size": logoSize,
            "company_id": company_id,
            "qrcode_color": qrcode_color,
            "product_name": product_name,
            "created_by": created_by,
            "is_active": is_active,
        }
        update_field = {
            "status":"nothing to update"
        }

        serializer = DoWellQrCodeSerializer(data=field)
        if serializer.is_valid():
            response = dowellconnection(*qrcode_management,"insert",field, update_field)
            return Response({"Response": response, "data": field}, status=status.HTTP_201_CREATED)
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





@method_decorator(csrf_exempt, name='dispatch')
class codeqrupdate(APIView):
    def put(self, request, id):

        company_id = request.data.get("company_id")
        link = request.data.get("link")
        logo = request.FILES.get('logo')
        logo_size = int(request.data.get("logo_size", "20"))
        qrcode_color = request.data.get('qrcode_color', "#000000")
        product_name = request.data.get("product_name")
        created_by = request.data.get("create_by")
        is_active = request.data.get("is_active", True)

        # Validate logo size
        try:
            logo_size = int(logo_size)
            if logo_size <= 0:
                raise ValueError("Logo size must be a positive integer.")
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
        if not is_valid_hex_color(qrcode_color):
            return Response({"error": "Invalid logo color. Must be a valid hex color code."}, status=status.HTTP_400_BAD_REQUEST)
        
        logo_image = resize_logo(logo, logo_size)
        # Create the QR code image
        img_qr = create_qrcode(link, qrcode_color)


        logo_base64 = logo_position(logo_image, img_qr)

        # Encode the QR code image to base64
        buffer = BytesIO()
        img_qr.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        logoSize = logo_size
        field = {
            "link": link,
            "logo": logo_base64,
            "qrcode": img_base64,
            "logo_size": logoSize,
            "company_id": company_id,
            "qrcode_color": qrcode_color,
            "product_name": product_name,
            "created_by": created_by,
            "is_active": is_active
        }
       
        update_field = {
            "status":"nothing to update"
        }

        serializer = DoWellUpdateQrCodeSerializer(data=field)
        if serializer.is_valid():
            response = dowellconnection(*qrcode_management,"insert",field, update_field)
            return Response({"Response":response, "data": field}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

           

 
      

