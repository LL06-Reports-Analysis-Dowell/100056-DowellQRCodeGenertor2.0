"""
This views deals with testing version of the application
"""
import json
import qrcode
import base64
from io import BytesIO
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from app.helper import *
from app.constant import *


@method_decorator(csrf_exempt, name='dispatch')
class testServerStatus(APIView):
    def get(self , request):
        return Response({"info":"QrCode Backend test servies running fine."}, status= status.HTTP_200_OK)