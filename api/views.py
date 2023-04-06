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
class codeqr(APIView):
    def post(self, request):
        link = request.data.get("link")
        logo = request.data.get("logo")

        qr_code = qrcode.QRCode(version=1, 
                            error_correction=qrcode.constants.ERROR_CORRECT_L, 
                            box_size=10, border=4)
        qr_code.add_data(logo)
        qr_code.make(fit=True)
        img_qr = qr_code.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img_qr.save(buffer, 'PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')


        field = {
            "link": link,
            "logo": logo,
            "qrcode": img_base64
        }
        update_field = {
            "name":request.data.get("name")
        }

        # buffer = BytesIO()
        # img_qr.save( format='PNG')

        response = dowellconnection(*qrcode_management,"update",field, update_field)
        return Response(json.loads(response), status=status.HTTP_201_CREATED)