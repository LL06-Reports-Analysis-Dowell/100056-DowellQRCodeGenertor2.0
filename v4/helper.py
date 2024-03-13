import io
import time
import uuid
import json
import re
from django.conf import settings
import qrcode
import requests
from PIL import Image, ImageDraw

import cloudinary.uploader
import cloudinary

from .serializers import DoWellQrCodeSerializer, LinkTypeSerializer, ProductTypeSerializer, VcardSerializer


cloudinary.config(
    cloud_name="din7lejen",
    api_key=835315697185388,
    api_secret="6uovHssSAvgpP-j82Z2qrra3bEE",
    api_proxy= 'http://proxy.server:3128'
)


def dowellconnection(cluster,database,collection,document,team_member_ID,function_ID,command,field,update_field):
    url = "http://uxlivinglab.pythonanywhere.com"
    payload = json.dumps({
        "cluster": cluster,
        "database": database,
        "collection": collection,
        "document": document,
        "team_member_ID": team_member_ID,
        "function_ID": function_ID,
        "command": command,
        "field": field,
        "update_field": update_field,
        "platform": "bangalore"
        })
    headers = {
        'Content-Type': 'application/json'
        }

    response = requests.request("POST", url, headers=headers, data=payload)
    res= json.loads(response.text)

    return res

def datacube_data_insertion(api_key, database_name, collection_name, data):
    """
    Insert data into a collection in the DataCube database.

    :param api_key: The API key for authentication.
    :param database_name: The name of the database.
    :param collection_name: The name of the collection.
    :param data: The data to be inserted into the collection.
    :return: The response text from the server.
    """
    url = "https://datacube.uxlivinglab.online/db_api/crud/"

    payload = {
        "api_key": api_key,
        "db_name": database_name,
        "coll_name": collection_name,
        "operation": "insert",
        "data": data,
        "payment": False
    }

    response = requests.post(url, json=payload)
    return response.text


def get_event_id():

    url="https://uxlivinglab.pythonanywhere.com/create_event"

    data={
        "platformcode":"FB" ,
        "citycode":"101",
        "daycode":"0",
        "dbcode":"pfm" ,
        "ip_address":"192.168.0.41", # get from dowell track my ip function 
        "login_id":"lav", #get from login function
        "session_id":"new", #get from login function
        "processcode":"1",
        "location":"22446576", # get from dowell track my ip function 
        "objectcode":"1",
        "instancecode":"100051",
        "context":"afdafa ",
        "document_id":"3004",
        "rules":"some rules",
        "status":"work",
        "data_type": "learn",
        "purpose_of_usage": "add",
        "colour":"color value",
        "hashtags":"hash tag alue",
        "mentions":"mentions value",
        "emojis":"emojis",
        "bookmarks": "a book marks"
    }

    r = requests.post(url,json=data)
    if r.status_code == 201:
        return json.loads(r.text)
    else: 
        return json.loads(r.text)['error']



def is_valid_hex_color(color):
    """
    Checks if the given string is a valid hex color code.
    """
    if not isinstance(color, str):
        return False
    if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
        return False
    return True

def create_qrcode(link, qrcode_color, logo = None):
    # create qr_code
    qr_code = qrcode.QRCode(
        version=1, 
        error_correction=qrcode.constants.ERROR_CORRECT_Q, 
        box_size=10, border=4
    )

    if not qrcode_color or qrcode_color == "" or qrcode_color == None:
        qrcode_color = "#000000"

    if link:
        qr_code.add_data(link)
    else:
        pass
    qr_code.make(fit=True)

    img_qr = qr_code.make_image(fill_color=qrcode_color, back_color="white").convert('RGB')
    
    if logo:
        logo_file = logo # Already converted to bytes in views.py
        basewidth = 100

        # Open the image using PIL's Image.open() method
        logo_image = Image.open(logo_file).convert("RGBA")

        # adjust image size
        wpercent = (basewidth/float(logo_image.size[0]))
        hsize = int((float(logo_image.size[1])*float(wpercent)))
        logo = logo_image.resize((basewidth, hsize), Image.ANTIALIAS)

        # Create a mask from the logo image
        logo_mask = Image.new("L", logo.size, 0)
        draw = ImageDraw.Draw(logo_mask)
        draw.ellipse((0, 0, hsize, hsize), fill=255)

        # set size of QR code
        pos = ((img_qr.size[0] - logo.size[0]) // 2,
                (img_qr.size[1] - logo.size[1]) // 2)
        
        img_qr.paste(logo, pos)
        
        img_qr = image_to_bytes(img_qr)
        return img_qr   
    img_qr = image_to_bytes(img_qr)
    return img_qr


def generate_file_name():
    timestamp = int(time.time())
    filename = f"qrcode_{timestamp}.jpg"
    return filename
   
def image_to_bytes(image):
    bytes_io = io.BytesIO()
    image.save(bytes_io, format='PNG')
    image_bytes = bytes_io.getvalue()
    return image_bytes

def upload_image_to_interserver(img, img_name=None):
    url = settings.INTERSERVER_URL
    files = {'file': (img_name, img)}
    response = requests.post(url, files=files)
    
    try:
        json_data = response.json()
        file_url = json_data.get("file_url")
        return file_url
    except json.JSONDecodeError as e:
        # Handle JSON decoding error
        print("Error decoding JSON response:", e)
    except KeyError as e:
        # Handle missing "file_url" key error
        print("Error accessing 'file_url' key:", e)
    


def update_cloudinary_image(image_url, your_updated_image_file):
    # Extract the public_id of the existing image from the image URL
    public_id = image_url.split('/')[-1].split('.')[0]

    # Upload the updated image to Cloudinary and retrieve the URL of the new image
    response = cloudinary.uploader.upload(your_updated_image_file, public_id=public_id)
    new_image_url = response['secure_url']
    return new_image_url



def create_uuid():
    unique_id = uuid.uuid1().int >> 64
    unique_id = str(unique_id)
    return unique_id



def qrcode_type_defination(qrcode_id_encrypted, iv_b64, qrcode_type, request, qrcode_color, logo, field, logo_url=None):
    serializer = None    
    if qrcode_type == "Product":
        title = request.data.get("title")
        product_name = request.data.get("product_name")
        website = request.data.get("website")
        product = {
            "product_name": product_name,
            "title": title,
            "website": website
        }
        field = {**field, **product}
        serializer = ProductTypeSerializer(data=field)

        # return serializer
        
    elif qrcode_type == "Vcard":
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        phone_number = request.data.get("phone_number")
        street_address = request.data.get("address.street_address")
        city = request.data.get("address.city")
        state = request.data.get("address.state")
        zip_code = request.data.get("address.zip_code")
        country = request.data.get("address.country")

        img_qr = create_qrcode(request.data, qrcode_color, logo)

        
        file_name = generate_file_name()
        qr_code_url = upload_image_to_interserver(img_qr, file_name)

        vcard = {
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "address": {
                "street_address": street_address,
                "city": city,
                "state": state,
                "zip_code": zip_code,
                "country": country,
            }
        }

        field = {**field, **vcard}
        serializer = VcardSerializer(data=field)

        # return serializer
        
    elif qrcode_type == "Link":
        link = request.data.get("link")
        # link = "https://100099.pythonanywhere.com/api/v1/inactive/"
        img_qr = create_qrcode(f"This QrCode is encrypted with {qrcode_id_encrypted} and {iv_b64} Decrypt it then Activate and Rescan.", qrcode_color, logo)

        file_name = generate_file_name()
        qr_code_url = upload_image_to_interserver(img_qr, file_name)
        link_ = {
            "link": link,
            "qrcode_image_url": qr_code_url,
            "logo_url": logo_url,
        }
        field = {**field, **link_}
        serializer = LinkTypeSerializer(data=field)

        # return serializer
        
    else:
        img_qr = create_qrcode(link=None, qrcode_color=qrcode_color, logo=logo)
        file_name = generate_file_name()
        qr_code_url = upload_image_to_interserver(img_qr, file_name)
        data = {
            "qrcode_image_url": qr_code_url,
            "logo_url": logo_url,
        }
        field = {**field, **data}
        serializer = DoWellQrCodeSerializer(data=field)
    return serializer, field



def processApikey(api_key):
    url = f'https://100105.pythonanywhere.com/api/v3/process-services/?type=api_service&api_key={api_key}'
    payload = {
        "service_id" : "DOWELL10007"
    }
    response = requests.post(url, json=payload)
    response_text = json.loads(response.text)
    return response_text