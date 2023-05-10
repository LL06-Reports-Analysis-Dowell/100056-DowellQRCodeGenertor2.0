import json
import requests

import re
from PIL import Image
import base64
import qrcode
import base64
from io import BytesIO
import io

import cloudinary

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

    r=requests.post(url,json=data)
    if r.status_code == 201:
        return json.loads(r.text)
    else: 
        return json.loads(r.text)['error']




def resize_logo(logo, logo_size):
    if logo_size:
        logo_size = int(logo_size)
    else:
        logo_size = 20
    if logo and logo.size > 0:
        logo_contents = logo.read()
        logo_image = Image.open(io.BytesIO(logo_contents))
        
        # Resize the logo to the desired size
        logo_image = logo_image.resize((logo_size, logo_size), resample=Image.LANCZOS)
        
    else:
        logo_image = None

    return logo_image

def is_valid_hex_color(color):
    """
    Checks if the given string is a valid hex color code.
    """
    if not isinstance(color, str):
        return False
    if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
        return False
    return True

def create_qrcode(link, qrcode_color):

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

    img_qr = qr_code.make_image(fill_color=qrcode_color, back_color="white")
    return img_qr

def logo_position(logo_image, img_qr):

    if logo_image:
           
        qrcode_logoSize = min(img_qr.size[0], img_qr.size[1]) * 25 // 100 
        logo_x = (img_qr.size[0] - qrcode_logoSize) // 2
        logo_y = (img_qr.size[1] - qrcode_logoSize) // 2

        # Resize the logo to the desired size
        logo_image = logo_image.resize((qrcode_logoSize, qrcode_logoSize), resample=Image.LANCZOS)

        # Paste the logo on the QR code image
        img_qr.paste(logo_image, (logo_x, logo_y))

        # Encode the logo image to base64
        buffer = BytesIO()
        logo_image.save(buffer, format="PNG")
        logo_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    else:
        logo_base64 = None

    return logo_base64





def get_base64_image(base64_image):
    # Decode the base64 encoded image
    image_data = base64.b64decode(base64_image)
    image = BytesIO(image_data)
    return image.getvalue()

def upload_image_to_cloudinary(img):
    #decode base64_image to bytes
    img = get_base64_image(img)

    cloudinary.config(
        cloud_name="din7lejen",
        api_key=835315697185388,
        api_secret="6uovHssSAvgpP-j82Z2qrra3bEE"
    )
    #upload image to cloudinary and return image_url
    upload_result = cloudinary.uploader.upload(img)
    image_url = upload_result.get('url')
    return image_url