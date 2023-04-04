import json
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
class DoWellQrCodeView(APIView):

    def post(self, request):
        logo = request.data.get("logo")
        product_name = request.data.get("product_name")
        link = request.data.get("link")
        company_id = request.data.get("company_id")
        create_by = request.data.get("create_by")

        # create a QRCODE with the logo field
        qr_code = qrcode.QRCode(version=1, 
                            error_correction=qrcode.constants.ERROR_CORRECT_L, 
                            box_size=10, border=4)
        qr_code.add_data(logo)
        qr_code.make(fit=True)
        img_qr = qr_code.make_image(fill_color="black", back_color="white")

        # Convert the image to a base64-encoded string
        buffer = BytesIO()
        img_qr.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        field = {
            "product_name":  product_name,
            "link": link,
            "company_id": company_id,
            "create_by" : create_by,
            "logo": logo,
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
    



@method_decorator(csrf_exempt, name='dispatch')
class test(APIView):

    def post(self, request):
        field = {
            "name":request.data.get("name"),
            "company_id":request.data.get("company_id")
        }
        update_field = {
            "status":"nothing to update"
        }
        response = dowellconnection(*qrcode_management,"insert",field, update_field)
        return Response(json.loads(response), status=status.HTTP_201_CREATED)
    
    def get(self,request,company_id):
        field = {
            "company_id":company_id,
        }
        update_field = {
            "status":"nothing to update"
        }
        response = dowellconnection(*qrcode_management,"fetch",field, update_field)
        return Response(json.loads(response), status=status.HTTP_201_CREATED)
    
    def put(self, request):
        field = {
            "id":request.data.get("id"),
            "name":request.data.get("name")
        }
        update_field = {
            "name":request.data.get("name")
        }
        response = dowellconnection(*qrcode_management,"update",field, update_field)
        return Response(json.loads(response), status=status.HTTP_201_CREATED)

