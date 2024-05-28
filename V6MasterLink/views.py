from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from datetime import datetime
from .dataCube import QR_code_datacube_data_insertion, datacube_data_retrieval,datacube_data_update
from .helper import create_uuid, qrcode_type_defination, upload_image_to_interserver, create_qrcode, generate_file_name, dowell_time
import uuid
import json
import requests
Apikey= '1b834e07-c68b-4bf6-96dd-ab7cdc62f07f'
QR_CODE_COLLECTION_NAME = 'qr_code_generate_collection'
MASTER_QR_CODE_COLLECTION_NAME = 'master_qr_code_collection'
DATABASE_NAME = 'qr_cdoe_generation'
class QRCodeAPIView(APIView):
    def get(self, request, qrcode_id):
        filter_data = {"qrcode_id": qrcode_id}

        response = datacube_data_retrieval(Apikey, DATABASE_NAME, QR_CODE_COLLECTION_NAME, filter_data)
        response = json.loads(response)

        if response['success'] and response['data']:
            return Response(response['data'][0], status=status.HTTP_200_OK)
        else:
            return Response({"error": "QR code not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
            num_qrcodes = request.data.get('num_qrcodes', 1)
            qrcode_type = request.data.get("qrcode_type")
            logo = request.FILES.get('logo')
            logo_size = int(request.data.get("logo_size", "20"))
            qrcode_color = request.data.get('qrcode_color', "#000000")
            created_by = request.data.get("created_by")
            lat= request.data.get("lat", "None")
            long = request.data.get("long", "None")
            is_active = request.data.get("is_active", False)
            playStoreLink = 'https://play.google.com/store/apps/details?id=com.dowellqrcodescanner.app&pli=1'
            redirect_link = request.data.get("redirect_link")
            qrcodes_created = []

            logo_file = None
            if logo:
                logo_file = logo.read()  # Converts InMemoryUploadedFile to bytes

            num_qrcodes = int(num_qrcodes) if int(num_qrcodes) > 0 else 1

            for _ in range(num_qrcodes):
                logo_url = None
                if logo_file:
                    logo_url = upload_image_to_interserver(logo_file, logo.name)
                qrcode_id = f'22-{str(uuid.uuid4())}'

                field = {
                    "qrcode_id": qrcode_id,
                    "logo_size": logo_size,
                    "qrcode_color": qrcode_color,
                    "created_by": created_by,
                    "lat": lat,
                    "long": long,
                    "is_active": is_active,
                    "qrcode_type": qrcode_type,
                    'playStoreLink': playStoreLink,
                    'redirect_link': redirect_link
                }

                serializer, field = qrcode_type_defination(qrcode_id, is_active, qrcode_type, request, qrcode_color,
                                                           logo, field, logo_url)
                print(field)
                if serializer.is_valid():
                    try:
                        print(Apikey)
                        response = QR_code_datacube_data_insertion(Apikey, DATABASE_NAME, QR_CODE_COLLECTION_NAME,
                                                                   field)
                        response = json.loads(response)
                        print(request)
                        if response['success']:
                            qrcodes_created.append(response['data']['inserted_id'])
                        else:
                            return Response({"error": response.get('message')},
                                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    except Exception as e:
                        return Response({"error": f"An error occurred: {str(e)}"},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"response": f"{num_qrcodes} QR codes created successfully.", "qrcodes": qrcodes_created},
                            status=status.HTTP_201_CREATED)
    
    def put(self, request, qrcode_id):
       
        filter_data = {"qrcode_id": qrcode_id}
        
        update_data = {
            "logo_size": request.data.get("logo_size"),
            "qrcode_color": request.data.get("qrcode_color"),
            "created_by": request.data.get("created_by"),
            "lat": request.data.get("lat"),
            "long": request.data.get("long"),
            "is_active": request.data.get("is_active"),
            "qrcode_type": request.data.get("qrcode_type"),
            "playStoreLink": request.data.get("playStoreLink"),
            "redirect_link": request.data.get("redirect_link"),
            "product_name": request.data.get("product_name"),
            "title": request.data.get("title"),
            "website": request.data.get("website")
        }

        update_data = {k: v for k, v in update_data.items() if v is not None}

        response = datacube_data_update(Apikey, DATABASE_NAME, QR_CODE_COLLECTION_NAME, filter_data, update_data)
        response = json.loads(response)

        if response['success']:
            return Response({"response": "QR code updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": response.get('message')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MasterQRCodeAPIView(APIView):
    def post(self, request):
        num_qrcodes = request.data.get('num_qrcodes', 1)
        created_by = request.data.get('created_by')
        data = {
            "created_by" : 'user12345',
        }
        response = datacube_data_retrieval(Apikey, DATABASE_NAME, QR_CODE_COLLECTION_NAME,data)
        response = json.loads(response)
        qrcode_list = response["data"]
        list_qr_id = []
        qrcodes_created = []
        if response['success']:
            for i in qrcode_list:
                list_qr_id.append({"qr_id":i["qrcode_id"]})
            master_qr_code_id = f'11-{str(uuid.uuid4())}'
            print(master_qr_code_id)
            field ={
                "master_qr_code_id":master_qr_code_id,
                "master_qr_code_link": None,
                "qr_code_ids": list_qr_id,
                "is_used":False
            }

            link = f"https://www.qrcodereviews.uxlivinglab.online/{master_qr_code_id}"
            logo = None
            qrcode_color ='#000000'
            img_qr = create_qrcode(link, qrcode_color, logo)
            file_name = generate_file_name()
            qr_code_url = upload_image_to_interserver(img_qr, file_name)
            link_ = {
                "master_qr_code_link": link,
                "master_qrcode_image_url": qr_code_url,
            }
            field = {**field, **link_}
            response = QR_code_datacube_data_insertion(Apikey, DATABASE_NAME, MASTER_QR_CODE_COLLECTION_NAME,
                                                       field)
            response = json.loads(response)
            print(request)
            if response['success']:
                qrcodes_created.append(response['data']['inserted_id'])
            else:
                return Response({"error": response.get('message')},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"response": f"master QR codes created successfully.", "qrcodes": qrcodes_created},
                        status=status.HTTP_201_CREATED)

    def put(self, request, master_qr_code_id):
        data = {
            "master_qr_code_id": master_qr_code_id
        }
        redirect_link = request.data.get('redirect_link')
        response = datacube_data_retrieval(Apikey, DATABASE_NAME, MASTER_QR_CODE_COLLECTION_NAME, data)
        response = json.loads(response)
        if not response['success']:
            return Response({"error": "Master QR code not found"}, status=status.HTTP_404_NOT_FOUND)
        master_qr_data = response['data']
        if not master_qr_data[0]['is_used']:
            qr_code_ids = [qr['qr_id'] for qr in master_qr_data[0]['qr_code_ids']]
            filters = {
                "qrcode_id": {"$in": qr_code_ids}
            }
            qr_code_data_response = datacube_data_retrieval(Apikey, DATABASE_NAME, QR_CODE_COLLECTION_NAME,
                                                              filters)
            qr_code_data_response = json.loads(qr_code_data_response)

            if not qr_code_data_response['success']:
                return Response({"error": "Failed to retrieve QR codes"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            qr_code_data_list = qr_code_data_response['data']
            qr_code_to_update = None
            for qr_code_data in qr_code_data_list:
                if not qr_code_data['is_active']:
                    qr_code_to_update = qr_code_data['qrcode_id']
                    break
            if qr_code_to_update:
                field = {
                    "qrcode_id":qr_code_to_update
                }
                update_data = {
                    "qrcode_id": qr_code_to_update,
                    "is_active": True,
                    "redirect_link":redirect_link
                }
                update_response = datacube_data_update(Apikey, DATABASE_NAME, QR_CODE_COLLECTION_NAME, field, update_data)
                update_response = json.loads(update_response)
                if not update_response['success']:
                    return Response({"error": f"Failed to update QR code {qr_code_to_update}"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            all_active = all(qr_code['is_active'] for qr_code in qr_code_data_list)

            if all_active:
                field = {
                    "master_qr_code_id": master_qr_code_id,
                }
                master_update_data = {
                    "master_qr_code_id": master_qr_code_id,
                    "is_used": True
                }
                master_update_response = datacube_data_update(Apikey, DATABASE_NAME, MASTER_QR_CODE_COLLECTION_NAME,
                                                              field,master_update_data)
                master_update_response = json.loads(master_update_response)
                if not master_update_response['success']:
                    return Response({"error": "Failed to update master QR code"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(qr_code_data_list)
        else:
            return Response({"error": "No QR code are available"}, status=status.HTTP_404_NOT_FOUND)
        

class CloneQRCodeAPIView(APIView):
    
    def post(self, request):
        data = {
            "master_qr_code_id": request.data.get("master_qr_code_id")
        }
        response = datacube_data_retrieval(Apikey, DATABASE_NAME, QR_CODE_COLLECTION_NAME, data)
        response = json.loads(response)
        if not response['success'] or not response['data']:
            return Response({"error": "Master QR code not found"}, status=status.HTTP_404_NOT_FOUND)

        master_qr_data = response['data'][0]

        clone_qrcode_id = f'clone-{str(uuid.uuid4())}'
        clone_data = {
            "clone_qrcode_id": clone_qrcode_id,
            "master_qrcode": data.get('master_qr_code_id'),
            "data": master_qr_data['data'],
            "created_at": master_qr_data['created_at'],
            "is_active": False
        }

        insert_response = QR_code_datacube_data_insertion(Apikey, DATABASE_NAME, QR_CODE_COLLECTION_NAME, clone_data)
        insert_response = json.loads(insert_response)

        if insert_response['success']:
            return Response({"response": "Cloned QR code created successfully.", "clone_qrcode_id": clone_qrcode_id},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"error": insert_response.get('message')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class QRCodeDataAPIView(APIView):
    def post(self, request):
        qrcode_id = request.data.get("qrcode_id")
        timezone = request.data.get('timezone', 'UTC')
        lat = request.data.get("lat")
        long = request.data.get("long")
        
        time_data = dowell_time(timezone)
        if 'error' in time_data:
            return Response({"error": "Failed to retrieve time from Dowell Clock"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        qrcode_id = f'33-{str(uuid.uuid4())}'
        new_qrcode_data = {
            "qrcode_id": qrcode_id,
            "time": time_data['current_time'],
            "lat": float(lat),
            "long": float(long),
        }

        insert_response = QR_code_datacube_data_insertion(Apikey, DATABASE_NAME, QR_CODE_COLLECTION_NAME, new_qrcode_data)
        insert_response = json.loads(insert_response)

        if insert_response['success']:
            return Response({"response": "QR code data saved successfully.", "qrcode_id": new_qrcode_data["qrcode_id"]},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"error": insert_response.get('message')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        