import json
import uuid
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .dataCube import QR_code_datacube_data_insertion, datacube_data_retrieval, datacube_data_update
from .helper import qrcode_type_defination, upload_image_to_interserver, create_qrcode, generate_file_name, dowell_time, check_the_post_under_required_lat_long

Apikey = '1b834e07-c68b-4bf6-96dd-ab7cdc62f07f'
QR_CODE_COLLECTION_NAME = 'qr_code_generate_collection'
MASTER_QR_CODE_COLLECTION_NAME = 'master_qr_code_collection'
QR_CODE_STAT_COLLECTION_NAME = 'Qr_code_stats'
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
        lat = request.data.get("lat", "None")
        long = request.data.get("long", "None")
        is_active = request.data.get("is_active", False)
        playStoreLink = 'https://play.google.com/store/apps/details?id=com.dowellqrcodescanner.app&pli=1'
        qrcodes_created = []
        qrcode_id = ""
        logo_file = None
        if logo:
            logo_file = logo.read()

        num_qrcodes = int(num_qrcodes) if int(num_qrcodes) > 0 else 1
        common_id = str(uuid.uuid4())
        for _ in range(num_qrcodes):
            logo_url = None
            if logo_file:
                logo_url = upload_image_to_interserver(logo_file, logo.name)
            qrcode_id = f'22-{str(uuid.uuid4())}'

            field = {
                "qrcode_id": qrcode_id,
                "generate_master_QR_code_id": common_id,
                "logo_size": logo_size,
                "qrcode_color": qrcode_color,
                "created_by": created_by,
                "lat": lat,
                "long": long,
                "is_active": is_active,
                "qrcode_type": qrcode_type,
                'playStoreLink': playStoreLink,
                'redirect_link': None
            }

            serializer, field = qrcode_type_defination(qrcode_id, is_active, qrcode_type, request, qrcode_color,
                                                       logo, field, logo_url)

            if serializer.is_valid():
                try:
                    print(Apikey)
                    response = QR_code_datacube_data_insertion(Apikey, DATABASE_NAME, QR_CODE_COLLECTION_NAME,
                                                               field)
                    response = json.loads(response)
                    print(request)
                    if response['success']:
                        qrcodes_created.append(field)
                    else:
                        return Response({"error": response.get('message')},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except Exception as e:
                    return Response({"error": f"An error occurred: {str(e)}"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"response": f"{num_qrcodes} QR codes created successfully.", "generate_master_QR_code_id": common_id,
             "qrcodes_data": qrcodes_created},
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
        }

        update_data = {k: v for k, v in update_data.items() if v is not None}

        response = datacube_data_update(Apikey, DATABASE_NAME, QR_CODE_COLLECTION_NAME, filter_data, update_data)
        response = json.loads(response)

        if response['success']:
            return Response({"response": "QR code updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": response.get('message')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, qrcode_id):
        filter_data = {"qrcode_id": qrcode_id}
        response = datacube_data_retrieval(Apikey, DATABASE_NAME, QR_CODE_COLLECTION_NAME, filter_data)
        response = json.loads(response)

        if response['success'] and response['data']:
            updated_data = {"is_active": False}
            delete_response = datacube_data_update(Apikey, DATABASE_NAME, QR_CODE_COLLECTION_NAME, filter_data, updated_data)
            delete_response = json.loads(delete_response)

            if delete_response['success']:
                return Response({"message": "QR code deleted successfully."}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"error": delete_response.get('message')},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "QR code not found"}, status=status.HTTP_404_NOT_FOUND)

class MasterQRCodeAPIView(APIView):
    def get(self, request):
        action = request.query_params.get('action')

        if action == 'master_qr_code_id':
            master_qr_code_id = request.query_params.get('master_qr_code_id')
            if not master_qr_code_id:
                return Response({"error": "Missing 'master_qr_code_id' parameter"}, status=status.HTTP_400_BAD_REQUEST)

            filter_data = {"master_qr_code_id": master_qr_code_id}
            response = datacube_data_retrieval(Apikey, DATABASE_NAME, MASTER_QR_CODE_COLLECTION_NAME, filter_data)
            response = json.loads(response)
            if response['success'] and response.get('data'):
                return Response(response['data'][0], status=status.HTTP_200_OK)
            else:
                return Response({"error": "Master QR code not found"}, status=status.HTTP_404_NOT_FOUND)

        elif action == 'created_by':
            created_by = request.query_params.get('created_by')
            if not created_by:
                return Response({"error": "Missing 'created_by' parameter"}, status=status.HTTP_400_BAD_REQUEST)

            qr_code_data = {"created_by": created_by}
            qr_codes_response = datacube_data_retrieval(Apikey, DATABASE_NAME, QR_CODE_COLLECTION_NAME, qr_code_data)
            qr_codes_response = json.loads(qr_codes_response)

            if not qr_codes_response['success']:
                return Response({"error": qr_codes_response.get('message', 'Failed to retrieve QR codes')},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            user_qr_ids = [qr['qrcode_id'] for qr in qr_codes_response['data']]

            master_qr_filter = {"qr_code_details.qr_id": {"$in": user_qr_ids}}
            master_qrs_response = datacube_data_retrieval(Apikey, DATABASE_NAME, MASTER_QR_CODE_COLLECTION_NAME, master_qr_filter)
            master_qrs_response = json.loads(master_qrs_response)

            if master_qrs_response['success']:
                return Response({"data": master_qrs_response['data']}, status=status.HTTP_200_OK)
            else:
                return Response({"error": master_qrs_response.get('message', f'Failed to retrieve master QR codes for user {created_by}')},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({"error": "Invalid or missing action parameter"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        id = request.data.get('generate_master_QR_code_id')
        data = {"generate_master_QR_code_id": id}
        email = request.data.get('email')
        name = request.data.get('name')
        location = request.data.get('location')
        description = request.data.get('description')

        response = datacube_data_retrieval(Apikey, DATABASE_NAME, QR_CODE_COLLECTION_NAME, data)
        response = json.loads(response)

        if not response['success']:
            return Response({"error": response.get('message')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        qrcode_list = response["data"]
        num_of_QR_Code = len(response["data"])
        list_qr_id = [{"qr_id": i["qrcode_id"], "qrcode_image_url": i["qrcode_image_url"], "link": i["link"], "is_active": i['is_active']} for i in qrcode_list]

        master_qr_code_id = f'11-{str(uuid.uuid4())}'
        field = {
            "master_qr_code_id": master_qr_code_id,
            "master_qr_code_link": None,
            "name": name,
            "location": location,
            "description": description,
            "is_used": False,
            "num_of_QR_Code": num_of_QR_Code,
            "qr_code_details": list_qr_id,

        }

        link = f"https://www.qrcodereviews.uxlivinglab.online/{master_qr_code_id}"
        logo = None
        qrcode_color = '#000000'
        img_qr = create_qrcode(link, qrcode_color, logo)
        file_name = generate_file_name()
        qr_code_url = upload_image_to_interserver(img_qr, file_name)

        field.update({
            "master_qr_code_link": link,
            "master_qrcode_image_url": qr_code_url,
        })

        response = QR_code_datacube_data_insertion(Apikey, DATABASE_NAME, MASTER_QR_CODE_COLLECTION_NAME, field)
        response = json.loads(response)

        if response['success']:
            return Response({"response": "Master QR code created successfully.", "master_qrcode": field},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"error": response.get('message')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, master_qr_code_id):
        data = {
            "master_qr_code_id": master_qr_code_id
        }
        if not master_qr_code_id.startswith("11"):
            return Response({"error": "Please Enter Correct Master QR Code ID"}, status=status.HTTP_404_NOT_FOUND)

        redirect_link = request.data.get('redirect_link')
        lat = request.data.get('lat')
        long = request.data.get('long')
        response = datacube_data_retrieval(Apikey, DATABASE_NAME, MASTER_QR_CODE_COLLECTION_NAME, data)
        response = json.loads(response)
        if not response['success']:
            return Response({"error": "Master QR code not found"}, status=status.HTTP_404_NOT_FOUND)
        master_qr_data = response['data']
        if not master_qr_data[0]['is_used']:
            qr_code_ids = [qr['qr_id'] for qr in master_qr_data[0]['qr_code_details']]
            filters = {
                "qrcode_id": {"$in": qr_code_ids}
            }
            qr_code_data_response = datacube_data_retrieval(Apikey, DATABASE_NAME, QR_CODE_COLLECTION_NAME, filters)
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
                    "qrcode_id": qr_code_to_update
                }
                update_data = {
                    "qrcode_id": qr_code_to_update,
                    "is_active": True,
                    "redirect_link": redirect_link,
                    "lat": lat,
                    "long": long,
                }
                update_response = datacube_data_update(Apikey, DATABASE_NAME, QR_CODE_COLLECTION_NAME, field,
                                                       update_data)
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
                                                              field, master_update_data)
                master_update_response = json.loads(master_update_response)
                if not master_update_response['success']:
                    return Response({"error": "Failed to update master QR code"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            update_data = {
                "name": request.data.get("name"),
                "location": request.data.get("location"),
                "description": request.data.get("description"),
            }
            update_data = {k: v for k, v in update_data.items() if v is not None}
            master_update_response = datacube_data_update(Apikey, DATABASE_NAME, MASTER_QR_CODE_COLLECTION_NAME, field,
                                                          update_data)
            master_update_response = json.loads(master_update_response)
            if master_update_response['success']:
                return Response({"message": "QR_code Data Activated Successfully"})
        else:
            return Response({"error": "No QR code are available"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, master_qr_code_id):
        filter_data = {"master_qr_code_id": master_qr_code_id}

        update_data = {
            "name": request.data.get("name"),
            "location": request.data.get("location"),
            "is_used": request.data.get("is_used"),
            "description": request.data.get("description"),
        }

        update_data = {k: v for k, v in update_data.items() if v is not None}

        if not update_data:
            return Response({"error": "No data provided to update"}, status=status.HTTP_400_BAD_REQUEST)

        response = datacube_data_retrieval(Apikey, DATABASE_NAME, MASTER_QR_CODE_COLLECTION_NAME, filter_data)
        response = json.loads(response)

        if not response['success'] or not response['data']:
            return Response({"error": "Master QR code not found"}, status=status.HTTP_404_NOT_FOUND)

        update_response = datacube_data_update(Apikey, DATABASE_NAME, MASTER_QR_CODE_COLLECTION_NAME, filter_data, update_data)
        update_response = json.loads(update_response)

        if update_response['success']:
            return Response({"response": "Master QR code updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": update_response.get('message')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        timezone = request.data.get('timezone')
        lat = request.data.get("lat")
        long = request.data.get("long")
        
        time_data = dowell_time(timezone)
        if 'error' in time_data:
            return Response({"error": "Failed to retrieve time from Dowell Clock"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        new_qrcode_data = {
            "qrcode_id": qrcode_id,
            "time": time_data['current_time'],
            "lat": float(lat),
            "long": float(long),
        }

        insert_response = QR_code_datacube_data_insertion(Apikey, DATABASE_NAME, QR_CODE_STAT_COLLECTION_NAME, new_qrcode_data)
        insert_response = json.loads(insert_response)

        if insert_response['success']:
            return Response({"response": "QR code data saved successfully.", "qrcode_id": new_qrcode_data["qrcode_id"]},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"error": insert_response.get('message')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get(self, request, qrcode_id):
        filter_data = {"qrcode_id": qrcode_id}

        response = datacube_data_retrieval(Apikey, DATABASE_NAME, QR_CODE_STAT_COLLECTION_NAME, filter_data)
        response = json.loads(response)
        data = response.get("data", [])

        detailed_report = []

        if data:
            for entry in data:
                detailed_report.append({
                    "qrcode_id": entry.get("qrcode_id"),
                    "lat": entry.get("lat"),
                    "long": entry.get("long"),
                    "scanned_at": entry.get("time")
                })
            success = True
            message = "The detailed report for qrcode scanner"
        else:
            success = False
            message = "No data found for the specified qrcode_id"

        report = {
            "success": success,
            "message": message,
            "response": {
                "total_scanned": len(data),
                "detailed_report": detailed_report
            }
        }
        return Response(report, status=status.HTTP_200_OK)

class FindQRCodeAPIView(APIView):
        def get(self, request):
            master_id = request.query_params.get('master_id')
            lat = request.query_params.get('lat')
            long = request.query_params.get('long')

            if not (master_id or (lat and long)):
                return Response({"success": False, "message": "Missing required fields"},
                                status=status.HTTP_400_BAD_REQUEST)
            filter_data = {}
            results = []
            if master_id:
                filter_data["master_qr_code_id"] = master_id
                response = datacube_data_retrieval(Apikey, DATABASE_NAME, MASTER_QR_CODE_COLLECTION_NAME, filter_data)
                response = json.loads(response)
                qr_codes = response['data'][0].get('qr_code_details', [])
                for data in qr_codes:
                    if data['lat'] == lat and data['long'] == long:
                        results.append(data)
                    else:
                        results.append(check_the_post_under_required_lat_long(float(lat), float(long), data['lat'], data['long']))

            if results:
                return Response({"success": True,"message": "location data", "response": results}, status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "message": "No records found"}, status=status.HTTP_404_NOT_FOUND)

def redirect_link(request, qrcode_id):
    if qrcode_id.startswith("11") or qrcode_id.startswith("22"):
        context = {'qrcode_id': qrcode_id}
        return render(request, 'redirect_linkv6.html', context)
    else:
        return Response("you Enter Wrong QR_code ID", status=status.HTTP_400_BAD_REQUEST)


class CreateQRCode(APIView):

    def post(self, request):
        try:
            num_qrcodes = int(request.data.get('num_qrcodes', 1))
            num_qrcodes = max(1, num_qrcodes)
            qrcode_type = request.data.get("qrcode_type")
            logo = request.FILES.get('logo')
            logo_size = int(request.data.get("logo_size", "20"))
            qrcode_color = request.data.get('qrcode_color', "#000000")
            created_by = request.data.get("created_by")
            lat = request.data.get("lat", "None")
            long = request.data.get("long", "None")
            is_active = request.data.get("is_active", False)
            email = request.data.get('email')
            name = request.data.get('name')
            location = request.data.get('location')
            description = request.data.get('description')
            playStoreLink = 'https://play.google.com/store/apps/details?id=com.dowellqrcodescanner.app&pli=1'

            qrcodes_created = []
            master_qr_code_id = f'11-{uuid.uuid4()}'
            common_id = str(uuid.uuid4())
            logo_file = logo.read() if logo else None

            for _ in range(num_qrcodes):
                logo_url = upload_image_to_interserver(logo_file, logo.name) if logo_file else None
                qrcode_id = f'22-{uuid.uuid4()}'

                field = {
                    "qrcode_id": qrcode_id,
                    'master_qr_code_id': master_qr_code_id,
                    "generate_master_QR_code_id": common_id,
                    "logo_size": logo_size,
                    "qrcode_color": qrcode_color,
                    "created_by": created_by,
                    "lat": lat,
                    "long": long,
                    "is_active": is_active,
                    "qrcode_type": qrcode_type,
                    'email': email,
                    'name': name,
                    'playStoreLink': playStoreLink,
                    'redirect_link': None
                }

                serializer, field = qrcode_type_defination(qrcode_id, is_active, qrcode_type, request, qrcode_color,
                                                           logo, field, logo_url)

                if serializer.is_valid():
                    response = QR_code_datacube_data_insertion(Apikey, DATABASE_NAME, QR_CODE_COLLECTION_NAME, field)
                    response = json.loads(response)
                    if response.get('success'):
                        qrcodes_created.append(field)
                    else:
                        return Response({"error": response.get('message')},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            master_field = {
                "master_qr_code_id": master_qr_code_id,
                "master_qr_code_link": None,
                "name": name,
                "location": location,
                "description": description,
                "is_used": False,
                "num_of_QR_Code": len(qrcodes_created),
                "qr_code_details": qrcodes_created,
            }

            link = f"https://www.qrcodereviews.uxlivinglab.online/{master_qr_code_id}"
            img_qr = create_qrcode(link, qrcode_color, None)
            file_name = generate_file_name()
            qr_code_url = upload_image_to_interserver(img_qr, file_name)

            master_field.update({
                "master_qr_code_link": link,
                "master_qrcode_image_url": qr_code_url,
            })

            response = QR_code_datacube_data_insertion(Apikey, DATABASE_NAME, MASTER_QR_CODE_COLLECTION_NAME,
                                                       master_field)
            response = json.loads(response)

            if response.get('success'):
                return Response({"response": "Master QR code created successfully.", "master_qrcode": master_field},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"error": response.get('message')},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)