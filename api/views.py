import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from database.connection import dowellconnection
from database.event import get_event_id
from database.database_management import *
from .serializers import OrderSerializer



@method_decorator(csrf_exempt, name='dispatch')
class test_database(APIView):

    def post(self, request ):
        name = request.data.get('name')
        description = request.data.get('description')
        company_id = request.data.get('company_id')
        if name and description and company_id:
            field = {
                "eventId":get_event_id()['event_id'],
                "name":  name,
                "description": description,
                "company_id": company_id
            }
            update_field = {
                "status":"nothing to update"
            }
            response = dowellconnection(*qrcode_management,"insert",field,update_field)
            print(response)
            return Response(json.loads(response),status=status.HTTP_201_CREATED)
        else:
            return Response({"INFO":"Error"},status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,company_id):
        if company_id:
            field = {
                "company_id": company_id
            }
            update_field = {
                "status":"nothing to update"
            }
            response = dowellconnection(*qrcode_management,"fetch",field,update_field)
            print(response)
            return Response(json.loads(response),status=status.HTTP_201_CREATED)
        else:
            return Response({"INFO":"Error"},status=status.HTTP_400_BAD_REQUEST)