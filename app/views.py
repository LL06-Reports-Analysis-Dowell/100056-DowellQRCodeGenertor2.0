import json
import qrcode
import base64
from io import BytesIO
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class serverStatus(APIView):
    def get(self , request):
        return Response({"info":"QrCode Backend servies running fine."}, status= status.HTTP_200_OK)
    
@method_decorator(csrf_exempt, name='dispatch')
class createQrCode(APIView):
    def post(self , request):
        name = request.data.get('name')
        return Response({"info":name}, status= status.HTTP_200_OK)
    
    def get(self, request , name):
        name = name 
        return Response({"info":name}, status= status.HTTP_200_OK)
