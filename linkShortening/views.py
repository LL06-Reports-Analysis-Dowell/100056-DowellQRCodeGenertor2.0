import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.urls import reverse

from .helper import has_query_params, retrieve_url_parameters, update_url_parameters


from .helper import (
    create_uuid, generate_file_name, is_valid_hex_color, create_qrcode,
    dowellconnection, qrcode_type_defination, update_cloudinary_image, 
    upload_image_to_interserver
)
from .constants import *

from .serializers import DoWellUpdateQrCodeSerializer, LinkSerializer, LinkFinalizeSerializer


@method_decorator(csrf_exempt, name='dispatch')
class serverStatus(APIView):
    def get(self, request):
        return Response({"info":"QrCode Backend servies running fine."}, status= status.HTTP_200_OK)
    
class Links(APIView):
    serializer_class = LinkSerializer

    def get_object(self, request, word, word2, word3):
        field = {"word": word, "word2": word2, "word3": word3}  
        res = dowellconnection(*qrcode_management, "fetch", field, {})
        response = json.loads(res)
        return response["data"]
        
    def post(self, request, word, word2, word3):
        r = self.get_object(request, word, word2, word3)
        if len(r) >= 1:
            return Response({"error": "Duplicate words"}, status=status.HTTP_400_BAD_REQUEST)
        
        link = request.data.get("link")
        api_key = request.data.get("api_key")
        link_id = request.data.get("link_id")
        # document_name = request.data.get("document_name")

        if not api_key:
            api_key = create_uuid()

        field = {
            "api_key": api_key,
            "link_id": link_id,
            # "document_name": document_name,
            "link": link,
            "is_active": True,
            "word": word,
            "word2": word2,
            "word3": word3
        }

        update_field = {

        }
       
        serializer = self.serializer_class(data=field)

        if serializer.is_valid(raise_exception=True):
            try:
                # insertion_thread = threading.Thread(target=self.mongodb_worker, args=(field, update_field))
                # insertion_thread.start()
                self.mongodb_worker(field, update_field)
                return Response({"response": field}, status=status.HTTP_201_CREATED)
            except:
                return Response({"error": "An error occurred while starting the insertion thread"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    def get(self, request, word, word2, word3):
        try:
            link_id = request.GET.get('link_id')
        except:
            pass

        update_field = {
            "is_active": True,
        }

        # get active links
        if word and word2 and word3:
            field = {"word": word, "word2": word2, "word3": word3, "is_active": True}
            try:
                res = dowellconnection(*qrcode_management, "fetch", field, {})
                response = json.loads(res)
            except:
                return Response({"error": "An error occurred when trying to access db"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # this will get inactive links
            if len(response["data"]) < 1:
                field2 = {"word": word, "word2": word2, "word3": word3, "is_active": False}
                res = dowellconnection(*qrcode_management, "fetch", field2, {})
                response = json.loads(res)
            
            # Check if there are any active links
            active_links = [link for link in response["data"] if link["is_active"]]

            print("Active Links", active_links)
            
            if len(active_links) > 0:

                # Select the first link
                open_link = active_links[0]

                # Update the "is_opened" status to True
                field = {"link_id": open_link["link_id"]}
                dowellconnection(*qrcode_management,"update",field, update_field)

                # Redirect to the open link and pass link_id to link
                if has_query_params(open_link["link"]):
                    return redirect(open_link["link"] + "&link_id=" + open_link["link_id"])
                else:
                    return redirect(open_link["link"] + "?link_id=" + open_link["link_id"])
                    
            else:
                # Check if there are any inactive links
                inactive_links = [link for link in response["data"] if not link["is_active"]]
                if len(inactive_links) > 0:
                    return render(request, 'return.html')

        # get single link using link_id
        elif link_id:
            field = {"link_id": link_id}
            try:
                res = dowellconnection(*qrcode_management, "fetch", field, {})
                return Response({"response": json.loads(res)}, status=status.HTTP_200_OK)
            except:
                return Response({"error": "An error occurred when trying to access db"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # return Response({"message": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
            return render(request, 'return.html', {'document_name': "None"})

        post_links_path = reverse('master_link', args=[word, word2, word3])
        post_links_url = request.build_absolute_uri(post_links_path)
        master_link = post_links_url
        return redirect(master_link)
    
    def mongodb_worker(self, field, update_field):
        dowellconnection(*qrcode_management,"insert", field, update_field)  

@api_view(['GET'])
def getLinks(request):
    vvs = request.GET.get("vvs")

    if vvs == "vvs":
        update_field = {
            "status":"nothing to update"
        }
        res = dowellconnection(*qrcode_management, "fetch", {}, update_field)
        return Response({"response": json.loads(res)}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "vvs required"}, status=400)
        


class codeqr(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        logo = request.FILES.get('logo') 
        qrcode_color = request.data.get('qrcode_color', "#000000")
        is_active = request.data.get('is_active', True)
        quantity = 1
        
        if not is_valid_hex_color(qrcode_color):
            return Response({"error": "Invalid logo color. Must be a valid hex color code."}, status=status.HTTP_400_BAD_REQUEST)
                 
        if logo:
            logo_file = logo.read() # This line affects the create_qrcode function below(converts InMemoryUploadedFile to bytes)     
        else:
            pass
        
        # chek if quantity is passed if not set to 1
        if quantity:
            quantity = int(quantity)
        else:
            quantity = 1
            
        for _ in range(quantity):
            logo_url = None

            if logo:
                logo_url = upload_image_to_interserver(logo_file, logo.name)
            else:
                logo_url = None

            field = {
                "qrcode_id": create_uuid(),
                "qrcode_color": qrcode_color,
                "is_active": is_active
            }

            update_field = {
                "status":"nothing to update"
            }

            # This function checks qrcode_type field and assign them appropriate properties
            serializer, field, duplicate_error = qrcode_type_defination(request, qrcode_color, logo, field, logo_url)

            if duplicate_error:
                return Response({"error": duplicate_error}, status=400)
            if serializer.is_valid(raise_exception=True):
                try:
                    # insertion_thread = threading.Thread(target=self.mongodb_worker, args=(field, update_field))
                    # insertion_thread.start()
                    self.mongodb_worker(field,update_field)
                except:
                    return Response({"error": "An error occurred while starting the insertion thread"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({"success": f"QR code created successfully.", "qrcode": field}, status=status.HTTP_201_CREATED)

     
    def mongodb_worker(self, field, update_field):
        dowellconnection(*qrcode_management,"insert", field, update_field)
    
    
    def get(self, request):
        try:
            company_id = request.GET.get('company_id')
            user_id = request.GET.get('user_id')
        except:
            pass

        if company_id:
            field = {"company_id": company_id}
        elif user_id:
            field = {"user_id": user_id}
        else:
            return Response({"error": "Pass company_id or user_id as querry parameter"}, status=404)
        
        # update_field = {"status": "nothing to update"}
        response = dowellconnection(*qrcode_management, "fetch", field, {})
        res = json.loads(response)
        if len(res["data"]):
            return Response({"response": res}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No qrcodes found"}, status=404)




@method_decorator(csrf_exempt, name='dispatch')
class codeqrupdate(APIView):
    
    def get_link(self, request, word, word2, word3):
        field = {"word": word, "word2": word2, "word3": word3}  
        res = dowellconnection(*qrcode_management, "fetch", field, {})
        response = json.loads(res)
        return response["data"]
    
    def get_object(self, request, id):
        field = {"qrcode_id": id}  
        res = dowellconnection(*qrcode_management, "fetch", field, {})
        response = json.loads(res)
        if response["isSuccess"]:
            return response["data"][0]
        
    
    def get(self, request, id):
        field = {"qrcode_id": id}  
        res = dowellconnection(*qrcode_management, "fetch", field, {})
        response = json.loads(res)

        # Check if the fetch was successful
        if response["isSuccess"]:
            return Response({"response": response["data"]}, status=status.HTTP_200_OK)
        else:
            return Response({"error": response["error"]}, status=status.HTTP_400_BAD_REQUEST)
   

    def put(self, request, id):
        try:
            qrcode_ = self.get_object(request, id)
            word, word2, word3 = retrieve_url_parameters(qrcode_["link"])
            param1 = request.data.get("word", word)
            param2 = request.data.get("word2", word2)
            param3 = request.data.get("word3", word3)

            print(param1, param2, param3)
            print(word, word2, word3)
            
            field = {"word": word, "word2": word2, "word3": word3}

            if param1 == word and param2 == word2 and param3 == word3:
                return self.update_qr_code(request, id, qrcode_, param1, param2, param3, field)
            else:
                r = self.get_link(request, param1, param2, param3)
                if len(r) >= 1 and param1 != word and param2 != word2 and param3 != word3:
                    return Response({"error": "Oops! Seems like the words have already been used."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return self.update_qr_code(request, id, qrcode_, param1, param2, param3, field)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update_qr_code(self, request, id, qrcode_, param1, param2, param3, field):
        try:
            link = request.data.get("link", qrcode_["link_"])
            master_link = qrcode_["link"]
            
            # update the Link
            try:
                update_field = {"word": param1, "word2": param2, "word3": param3, "link": link}
                dowellconnection(*qrcode_management,"update",field, update_field)
            except:
                return Response({"error": "Update Link Failed"}, status=status.HTTP_400_BAD_REQUEST)
            
            # update the Qrcode
            field_qrcode = {"qrcode_id": id} 
            try:
                update_field = {"word": param1, "word2": param2, "word3": param3, "link_": link}
                dowellconnection(*qrcode_management,"update", field_qrcode, update_field)
                if param1 or param2 or param3:
                    master_link = update_url_parameters(master_link, param1, param2, param3)
            except:
                return Response({"error": f"Update Qrcode Failed {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
            


            qrcode_color = request.data.get('qrcode_color', qrcode_["qrcode_color"])
            logo = request.FILES.get('logo')
            logo_url = self.validate_logo(logo, qrcode_["logo_url"])

            # Create the QR code image
            img_qr = create_qrcode(master_link, qrcode_color, logo)

            # Update qrcode and logo image in cloudinary
            file_name = generate_file_name()
            qrcode_image_url = upload_image_to_interserver(img_qr, file_name)

            field = {"qrcode_id": id}
            update_field = {
                "user_id": qrcode_["user_id"],
                "company_id": qrcode_["company_id"],
                "is_active": request.data.get("is_active", qrcode_["is_active"]),
                "qrcode_color": qrcode_color,
                "link": master_link,
                "link_": link,
                "word": param1,
                "word2": param2,
                "word3": param3,
                "logo_url": logo_url,
                "qrcode_image_url": qrcode_image_url,
            }

            serializer = DoWellUpdateQrCodeSerializer(data=update_field)
            if serializer.is_valid():
                res = dowellconnection(*qrcode_management, "update", field, update_field)
                response = json.loads(res)

                if response["isSuccess"]:
                    success = {"success": f"QR code Updated successfully.", "response": update_field}
                    # return success
                    return Response(success, status=status.HTTP_200_OK)
                else:
                    error = {"error": response["error"]}
                    # return = error
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def validate_logo(self, logo, logo_url):
        # Your code for validating logo size and updating the logo_url here
        if not logo and not logo_url:
            logo_url = None
        elif not logo_url and logo:
            logo_file = logo.read()
            logo_url = upload_image_to_interserver(logo_file, logo.name)
        elif logo_url and logo:
            logo_url = upload_image_to_interserver(logo, logo.name)
        else:
            pass
        return logo_url

    











