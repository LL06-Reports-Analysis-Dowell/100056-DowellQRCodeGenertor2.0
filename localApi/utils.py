import re
from PIL import Image
import base64
import qrcode
import base64
from io import BytesIO
import io


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