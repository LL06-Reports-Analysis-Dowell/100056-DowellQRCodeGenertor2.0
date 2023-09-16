import base64
import io
import time
from urllib.parse import urlparse
import uuid
import json
import re
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlparse


import qrcode
import requests
from PIL import Image, ImageDraw

import cloudinary.uploader
import cloudinary

from .serializers import DoWellQrCodeSerializer, LinkSerializer

cloudinary.config(
    cloud_name="din7lejen",
    api_key=835315697185388,
    api_secret="6uovHssSAvgpP-j82Z2qrra3bEE",
    api_proxy= 'http://proxy.server:3128'
)

# check if link has query params or not
def has_query_params(url):
    parsed_url = urlparse(url)
    query_params = parsed_url.query

    if query_params or parsed_url.fragment:
        return True
    else:
        return False

def linkConnection(cluster,database,collection,document,team_member_ID,function_ID,command,field,update_field):
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



def urlParse(url: str):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split("/")
    last_path_part = path_parts[-1]
    return last_path_part

def create_short_uuid():
    uuid_value = uuid.uuid4().bytes
    base64_encoded = base64.urlsafe_b64encode(uuid_value).rstrip(b'=')

    # Get the current timestamp (in seconds) and convert it to base64
    current_timestamp = int(time.time())
    timestamp_bytes = str(current_timestamp).encode('utf-8')
    # timestamp_base64 = base64.urlsafe_b64encode(timestamp_bytes).rstrip(b'=')
    # Combine the short UUID and timestamp component
    combined_uuid = base64_encoded[:4] + base64_encoded[-4:]
    return combined_uuid.decode('utf-8')  # Convert bytes back to string

def is_valid_hex_color(color):
    """
    Checks if the given string is a valid hex color code.
    """
    if not isinstance(color, str):
        return False
    if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
        return False
    return True


def create_qrcode(link, qrcode_color, logo):
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
        logo_image = Image.open(logo_file)

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

    try:
        response = requests.post(url, files=files)
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Looks Like you are offline")
    
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

def retrieve_url_parameters(url):
    # Parse the URL to extract the query parameters
    url_segments = url.strip('/').split('/')

    # Assign the segments to variables 'word', 'word1', and 'word2'
    if len(url_segments) >= 3:
        word = url_segments[-3]
        word2 = url_segments[-2]
        word3 = url_segments[-1]
        return word, word2, word3
    else:
        print("Invalid URL format")

def update_url_parameters(url, word, word1, word2):
    # Split the URL path into segments using '/'
    url_segments = url.split('/')

    # Ensure there are at least three segments in the URL
    if len(url_segments) >= 3:
        url_segments[-3] = word
        url_segments[-2] = word1
        url_segments[-1] = word2
    else:
        # Handle the case where the URL doesn't have enough segments
        return "Invalid URL format"

    # Reconstruct the URL with the updated path segments
    updated_url = '/'.join(url_segments)

    # Now you can use the updated_url in your view logic or return it
    return updated_url

def qrcode_type_defination(request, qrcode_color, logo, field, logo_url=None):
    serializer = None    

    # links = request.data["links"]
    user_id = request.data.get("user_id")
    company_id = request.data.get("company_id")
    link = request.data.get("link")
    word  = create_short_uuid()
    word2 = create_short_uuid()
    word3 = create_short_uuid()

    # document_name = request.data.get("document_name")

    # get master link
    api_key = create_uuid()
    post_links_path = reverse('master_link', args=[word, word2, word3])

    post_links_url  = request.build_absolute_uri(post_links_path)

    posted_links = []
    duplicate_error = None

    link_id = create_uuid()
    link_data = {
        "link_id": link_id, 
        "api_key": api_key,  
        "link": link,
        "word": word,
        "word2": word2,
        "word3": word3
    }

    link_serializer = LinkSerializer(data=link_data)
    if link_serializer.is_valid(raise_exception=True):
        res = requests.post(post_links_url, link_data)
        if res.status_code == 201:
            posted_links.append(res.json())
        else:
            duplicate_error = "Oops! Seems like the words have already been used."

    # get all posted links
    master_link = post_links_url

    img_qr = create_qrcode(master_link, qrcode_color, logo)

    file_name = generate_file_name()
    qr_code_url = upload_image_to_interserver(img_qr, file_name)

    
    link_ = {
        "company_id": company_id,
        "user_id": user_id,
        "link": master_link,
        "qrcode_image_url": qr_code_url,
        "logo_url": logo_url,
        "link_": link,
        "word": word,
        "word2": word2,
        "word3": word3
    }

    serializer = DoWellQrCodeSerializer(data=request.data)
    
    field = {**field, **link_}
    return serializer, field, duplicate_error


