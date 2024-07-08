import qrcode
from django.conf import settings
import qrcode
import requests
import io
import json
from PIL import Image, ImageDraw
import uuid
from .serializers import DoWellQrCodeSerializer, LinkTypeSerializer, ProductTypeSerializer, VcardSerializer
import time
from math import radians, sin, cos, sqrt, atan2
def image_to_bytes(image):
    bytes_io = io.BytesIO()
    image.save(bytes_io, format='PNG')
    image_bytes = bytes_io.getvalue()
    return image_bytes


def generate_file_name():
    timestamp = int(time.time())
    filename = f"qrcode_{timestamp}.jpg"
    return filename


def create_qrcode(link, qrcode_color, logo=None):
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
        logo_file = logo  # Already converted to bytes in views.py
        basewidth = 100

        # Open the image using PIL's Image.open() method
        logo_image = Image.open(logo_file).convert("RGBA")

        # adjust image size
        wpercent = (basewidth / float(logo_image.size[0]))
        hsize = int((float(logo_image.size[1]) * float(wpercent)))
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



def create_uuid():
    unique_id = uuid.uuid4()
    unique_id = str(unique_id)
    return unique_id


def qrcode_type_defination(qrcode_id_encrypted, is_active, qrcode_type, request, qrcode_color, logo, field,
                           logo_url=None):
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
        link = f"https://www.qrcodereviews.uxlivinglab.online/{field['qrcode_id']}"

        img_qr = create_qrcode(link, qrcode_color, logo)
        file_name = generate_file_name()
        qr_code_url = upload_image_to_interserver(img_qr, file_name)
        link_ = {
            "link": link,
            "qrcode_image_url": qr_code_url,
            "logo_url": logo_url,
        }
        field = {**field, **link_}
        serializer = LinkTypeSerializer(data=field)

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

def dowell_time(timezone):
        """
        Fetches current time from Dowell Clock API for the specified timezone.

        :param timezone: The timezone for which to fetch the current time.
        :return: A dictionary containing the response from the API, including the current time.
        """
        
        url = "https://100009.pythonanywhere.com/dowellclock/"
        payload = json.dumps({
            "timezone":timezone,
            })
        headers = {
            'Content-Type': 'application/json'
            }

        response = requests.request("POST", url, headers=headers, data=payload)
        res= json.loads(response.text)

        return res


def check_the_post_under_required_lat_long(lat1, lon1, lat2, lon2):
    R = 6371000
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance < 5