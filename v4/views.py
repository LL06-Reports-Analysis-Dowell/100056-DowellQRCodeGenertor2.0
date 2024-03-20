import base64
import json
import threading
from django.shortcuts import render
from v4.dataCube import QR_code_datacube_data_insertion, datacube_data_retrieval, datacube_data_update
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.settings import Apikey, DATABASE_NAME, COLLECTION_NAME
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .helper import (
    create_uuid, datacube_data_insertion, decode_base64_url_safe, decrypt_qrcode_id, encode_base64_url_safe, encrypt_qrcode_id, generate_file_name, is_valid_hex_color,
    create_qrcode,
    dowellconnection, processApikey, qrcode_type_defination, update_cloudinary_image,
    upload_image_to_interserver
)
from .constant import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode
import os

from Crypto.Util.Padding import unpad
from base64 import b64decode

from .serializers import DoWellActivateQrCodeSerializer, DoWellUpdateQrCodeSerializer


# Secret key for encryption (make sure to keep it secure)


def inactive(request):
    return render(request, template_name='inactive_qrcode.html')


@method_decorator(csrf_exempt, name='dispatch')
class serverStatus(APIView):
    def get(self, request):
        return Response({"info": "QrCode Backend servies running fine."}, status=status.HTTP_200_OK)


class codeqr(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        # api_key = request.GET.get('api_key')

        company_id = request.data.get("company_id")
        qrcode_type = request.data.get("qrcode_type")

        master_link = request.data.get("master_link")
        product_name = request.data.get("product_name")
        logo = request.FILES.get('logo')
        logo_size = int(request.data.get("logo_size", "20"))
        qrcode_color = request.data.get('qrcode_color', "#000000")

        created_by = request.data.get("created_by")
        description = request.data.get("description")
        is_active = request.data.get("is_active", False)
        quantity = request.data.get("quantity")

        try:
            if logo_size <= 0:
                raise ValueError("Logo size must be a positive integer.")
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not is_valid_hex_color(qrcode_color):
            return Response({"error": "Invalid logo color. Must be a valid hex color code."},
                            status=status.HTTP_400_BAD_REQUEST)

        if logo:
            logo_file = logo.read()  # This line affects the create_qrcode function below(converts InMemoryUploadedFile to bytes)
        else:
            pass

        qrcodes_created = []

        # chek if quantity is passed if not set to 1
        if int(quantity) > 0:
            quantity = int(quantity)
        else:
            quantity = 1

        for _ in range(quantity):
            logo_url = None

            if logo:
                logo_url = upload_image_to_interserver(logo_file, logo.name)
            else:
                logo_url = None

            qrcode_id = create_uuid()
            encrypted_qrcode_id, iv = encrypt_qrcode_id(qrcode_id)

            # qrcode_id_encrypted = base64.b64encode(encrypted_qrcode_id).decode('utf-8')
            # iv_b64 = base64.b64encode(iv).decode('utf-8')
            qrcode_id_encrypted = encode_base64_url_safe(encrypted_qrcode_id)
            iv_b64 = encode_base64_url_safe(iv)

            field = {
                "master_link": master_link,
                "qrcode_id": qrcode_id_encrypted,
                "iv": iv_b64,
                "qrcode_id_decrypted": qrcode_id,
                "logo_size": logo_size,
                "qrcode_color": qrcode_color,
                "company_id": company_id,
                "created_by": created_by,
                "description": description,
                "product_name": product_name,
                "is_active": is_active,
                "qrcode_type": qrcode_type,
            }

            update_field = {
                "status": "nothing to update"
            }

            # Encrypt the data before embedding it into the QR code

            # This function checks qrcode_type field and assign them appropriate properties
            serializer, field = qrcode_type_defination(qrcode_id_encrypted, iv_b64, qrcode_type, request, qrcode_color,
                                                       logo, field, logo_url)

            # qrcodes_created.append(field)
            if serializer.is_valid():
                try:
                    print(Apikey)
                    data = QR_code_datacube_data_insertion(Apikey, DATABASE_NAME, COLLECTION_NAME, field)
                    print(data)
                    # insertion_thread = threading.Thread(target=self.mongodb_worker, args=(field, update_field))
                    # insertion_thread.start()
                    # return Response({"response": field}, status=status.HTTP_201_CREATED)
                except:
                    return Response({"error": "An error occurred while starting the insertion thread"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                del field["master_link"]
                del field["link"]
                qrcodes_created.append(field)

        if qrcodes_created:
            return Response({"response": f"{quantity} QR codes created successfully.", "qrcodes": qrcodes_created},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # else:

    #     return Response(response_text, status=status.HTTP_400_BAD_REQUEST)



class DecryptQRCode(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


    def post(self, request):
        encrypted_qrcode_id_b64 = request.data.get("qrcode_id")
        iv_b64 = request.data.get("iv")


        encrypted_qrcode_id = base64.urlsafe_b64decode(encrypted_qrcode_id_b64)
        iv = decode_base64_url_safe(iv_b64)


        # Decrypt the encrypted QR code ID back to its original UUID
        decrypted_qrcode_id = decrypt_qrcode_id(encrypted_qrcode_id, iv)


        # Convert the UUID to string for readability
        decrypted_qrcode_id_str = str(decrypted_qrcode_id)[2:-1]


        return Response({"qrcode_id": decrypted_qrcode_id_str}, status=status.HTTP_200_OK)

# class DecryptQRCode(APIView):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def post(self, request):
#         encrypted_qrcode_id_b64 = request.data.get("qrcode_id")
#         iv_b64 = request.data.get("iv")

#         encrypted_qrcode_id = base64.urlsafe_b64decode(encrypted_qrcode_id_b64)
#         iv = decode_base64_url_safe(iv_b64)

#         # Decrypt the encrypted QR code ID back to its original UUID
#         decrypted_qrcode_id = decrypt_qrcode_id(encrypted_qrcode_id, iv)

#         # Convert the UUID to string for readability
#         decrypted_qrcode_id_str = str(decrypted_qrcode_id)[2:-1]

#         field = {"qrcode_id_decrypted": decrypted_qrcode_id_str}
#         response = datacube_data_retrieval(Apikey, DATABASE_NAME, COLLECTION_NAME, field)
#         res = json.loads(response)
#         qrcode_list = res["data"]

#         return Response({"Data": qrcode_list}, status=status.HTTP_200_OK)

    def database_worker(self, field, update_field):
        datacube_data_insertion(*qrcode_management, "insert", field, update_field)

    def get(self, request):
        created_by = request.GET.get('id')
        print(created_by)
        field = {"qrcode_id_decrypted": created_by}
        if created_by:
            response = datacube_data_retrieval(Apikey, DATABASE_NAME, COLLECTION_NAME, field)
        else:
            response = datacube_data_retrieval(Apikey, DATABASE_NAME, COLLECTION_NAME, field)

        res = json.loads(response)
        qrcode_list = res["data"]
        for item in qrcode_list:
            try:
                del item["master_link"]
            except:
                pass
            del item["link"]

        if len(qrcode_list) < 1:
            return Response({"message": f"no qrcodes found created by {created_by}"}, status=400)
        return Response({"response": res}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class codeqrupdate(APIView):

    def get_object(self, request, id):
        field = {"qrcode_id": id}
        res = datacube_data_retrieval(Apikey, DATABASE_NAME, COLLECTION_NAME, field)
        # res = dowellconnection(*qrcode_management, "fetch", field, {})
        response = json.loads(res)

        if response["success"]:
            return response["data"][0]

    def get(self, request, id):
        field = {"qrcode_id": id}
        res = datacube_data_retrieval(Apikey, DATABASE_NAME, COLLECTION_NAME, field)
        # res = dowellconnection(*qrcode_management, "fetch", field, {})
        response = json.loads(res)

        data = response["data"]

        # Check if the fetch was successful
        if response["success"] and len(data) > 0:
            del data[0]["master_link"]
            del data[0]["link"]

            return Response({"response": data}, status=status.HTTP_200_OK)
        elif len(response["data"]) < 1:
            return Response({"error": "no qrcodes found with given id"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": response["error"]}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        # get cloudinary qrcode image in order to update it
        logo_url = ""

        try:
            qrcode_ = self.get_object(request, id)
            qrcode_image_url = qrcode_.get("qrcode_image_url", "")
            logo_url = qrcode_.get("logo_url", "")
        except:
            return Response({"error": "No qrcodes found with given id"}, status=status.HTTP_404_NOT_FOUND)

        company_id = request.data.get("company_id", qrcode_["company_id"])
        link = request.data.get("link", qrcode_["link"])

        try:
            master_link = request.data.get("master_link", qrcode_["master_link"])
        except:
            master_link = request.data.get("master_link")

        if not master_link:
            return Response({"message": "Masterlink not found master_link in required"})

        logo = request.FILES.get('logo')
        logo_size = int(request.data.get("logo_size", "20"))

        try:
            product_name = request.data.get('product_name', qrcode_["product_name"])
        except:
            product_name = request.data.get('product_name')

        qrcode_color = request.data.get('qrcode_color', qrcode_["qrcode_color"])
        created_by = request.data.get("created_by", qrcode_["created_by"])
        description = request.data.get("description", qrcode_["description"])
        is_active = request.data.get("is_active", qrcode_["is_active"])

        # Validate logo size
        try:
            if logo_size <= 0:
                raise ValueError("Logo size must be a positive integer.")
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not is_valid_hex_color(qrcode_color):
            return Response({"error": "Invalid logo color. Must be a valid hex color code."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not logo and not logo_url:
            logo_url = None
        elif not logo_url and logo:
            logo_file = logo.read()
            logo_url = upload_image_to_interserver(logo_file, logo.name)
        elif logo_url and logo:
            # logo_url = update_cloudinary_image(logo_url, logo)
            logo_url = upload_image_to_interserver(logo, logo.name)
        else:
            pass

        # Create the QR code image/ Check if is_active is True and put masterlink
        if is_active == True:
            img_qr = create_qrcode(master_link, qrcode_color, logo)
            file_name = generate_file_name()
            qrcode_image_url = upload_image_to_interserver(img_qr, file_name)
        else:
            if logo:
                img_qr = create_qrcode(f"This QrCode with ID {id} has been deactivated. Reactivate and Rescan.",
                                       qrcode_color, logo)
                file_name = generate_file_name()
                qrcode_image_url = upload_image_to_interserver(img_qr, file_name)
            else:
                img_qr = create_qrcode(f"This QrCode with ID {id} has been deactivated. Reactivate and Rescan.",
                                       qrcode_color)
                file_name = generate_file_name()
                qrcode_image_url = upload_image_to_interserver(img_qr, file_name)

        logoSize = logo_size

        field = {
            "qrcode_id": id
        }

        update_field = {
            "qrcode_id": id,
            "logo_size": logoSize,
            "product_name": product_name,
            "qrcode_color": qrcode_color,
            "master_link": master_link,
            "company_id": company_id,
            "created_by": created_by,
            "description": description,
            "is_active": is_active,
            "qrcode_type": qrcode_["qrcode_type"],
            "qrcode_image_url": qrcode_image_url,
            "logo_url": logo_url
        }

        serializer = DoWellUpdateQrCodeSerializer(data=update_field)
        if serializer.is_valid():
            # res = dowellconnection(*qrcode_management,"update",field, update_field)
            res = datacube_data_update(Apikey, DATABASE_NAME, COLLECTION_NAME, field, update_field)
            response = json.loads(res)

            # Check if the update was successful
            if response["success"]:
                del update_field["master_link"]
                return Response({"response": update_field, "message": "Qrcode Updated Successfully"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": response["error"]}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class codeqractivate(APIView):

    def get_object(self, request, id):
        field = {"qrcode_id": id}
        res = datacube_data_retrieval(Apikey, DATABASE_NAME, COLLECTION_NAME, field)
        # res = dowellconnection(*qrcode_management, "fetch", field, {})
        response = json.loads(res)

        if response["success"]:
            return response["data"][0]

    def put(self, request, id):
        logo = request.FILES.get('logo')
        field = {
            "qrcode_id": id
        }

        try:
            qrcode_ = self.get_object(request, id)
            qrcode_master_link = qrcode_["master_link"]
            qrcode_logo_url = qrcode_["logo_url"]
            qrcode_color = qrcode_["qrcode_color"]
        except:
            return Response({"error": "no qrcodes found with given id"}, status=status.HTTP_404_NOT_FOUND)

        img_qr = create_qrcode(qrcode_master_link, qrcode_color, logo)

        # update qrcode and logo image in cloudinary
        file_name = generate_file_name()
        qrcode_image_url = upload_image_to_interserver(img_qr, file_name)

        update_field = {
            "is_active": True,
            "qrcode_image_url": qrcode_image_url
        }

        # res = dowellconnection(*qrcode_management, "update", field, update_field)
        res = datacube_data_update(Apikey, DATABASE_NAME, COLLECTION_NAME, field, update_field)
        response = json.loads(res)

        data = self.get_object(request, id)

        # Check if the update was successful
        if response["success"]:
            del data["master_link"]
            del data["link"]
            return Response({"response": data, "message": "Qrcode activated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": response["error"]}, status=status.HTTP_400_BAD_REQUEST)
