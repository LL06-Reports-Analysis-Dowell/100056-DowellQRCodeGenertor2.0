import re
from PIL import Image
import base64
import qrcode
import base64
from io import BytesIO
import io
import pyshorteners

def change_image_color_(image_path, new_color):
    # Load the image
    image = Image.open(image_path)

    # Convert the image to RGBA mode
    image = image.convert("RGBA")

    # Get the width and height of the image
    width, height = image.size

    # Create a new blank image of the same size and mode as the original image
    new_image = Image.new("RGBA", (width, height), color=(0, 0, 0, 0))

    # Loop through each pixel in the image and change its color
    for x in range(width):
        for y in range(height):
            # Get the current pixel color
            current_color = image.getpixel((x, y))

            # Check if the current pixel color is not transparent
            if current_color[3] != 0:
                # Create a new color tuple with the specified color and alpha
                new_color_with_alpha = tuple(int(new_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (current_color[3],)

                # Replace the current pixel color with the new color
                new_image.putpixel((x, y), new_color_with_alpha)

    # Return the modified image
    return new_image


def resize_image(image_path, size):
    """
    Resizes the image at the given path to the given size.
    """
    # Open the image
    with Image.open(image_path) as image:
        # Calculate the new size
        width, height = image.size
        new_size = (int(size * width), int(size * height))
        # Resize the image
        resized_image = image.resize(new_size)
        # Return the resized image
        return resized_image

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

    qr_code = qrcode.QRCode(version=1, 
                                error_correction=qrcode.constants.ERROR_CORRECT_Q, 
                                box_size=10, border=4)
        
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