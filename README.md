# 100056-DowellQRCodeGenertor2.0

## API Documentation 

created a post request method

created a Qrcode with the logo field

After generating the Qrcode it Convert the image to a base64-encoded string and save the datas to the database

## Creating a QR code using Python Django

In this ReadMe file, we will be creating a simple QR code generator using Python Django. 

## Prerequisites

Before you begin, make sure you have the following software installed on your computer:
    .Python 3.7+
    
## Step 1: Setting up the Django project in your local machine
    
    Clone project by running the following command in your terminal:
    *git clone git@github.com:LL06-Reports-Analysis-Dowell/100056-DowellQRCodeGenertor2.0.git

## Next, get into the Projects directory:

    Get into the projects directory by running:
    *cd /100056-DowellQRCodeGenertor2.0

    Create a virtual enviroment and activate it in the terminal using
    *python3 -m venv venve
    *source venve/bin/activate - linux

## Install the requirements

    *pip install -r requirements.txt

## Create a QRcode:
    POST REQUEST : http://127.0.0.1:8000/api/codeqr/
    This should be a form data:
    {
        company_id : "example-company", - required
        logo: "image.png", -optional
        logo_size: "23", -optional defaults to 20 
        qrcode_color: "#009933" - optional
    }

    The response will be:
    {
        "logo": "base64_string",
        "qrcode: "base64_string"
        "link": null,
        "company_id": "example-company",
        "logo_size": "20",
        "qrcode_color": null,
        "is_active": false
    }
    
    
## Update the Qrcode with Following Input Fields:
    PUT REQUEST: http://127.0.0.1:8000/api/dowell_codeqrupdate/<str:company_id>

    link: "https://example.com" - required
    company_id: "example1company" - optional
    qrcode_color: "#ff0000" - optional
    logo: "image.png"   - optional

    The response will be:
    {
        "logo": "base64_string",
        "qrcode: "base64_string"
        "link": "https://example.com",
        "company_id": "example-company",
        "logo_size": "20",
        "qrcode_color": "#ff0000",
        "product_name": "name",
        "created_by": "ayush" 
        "is_active": true
    }


## Fetch the QRcode using Company_id as Query parameter:

    GET REQUEST : http://127.0.0.1:8000/api/dowell_codeqr/?company_id=company_id

    The response:
    {
        "logo": "base64_string",
        "qrcode: "base64_string"
        "link": "https://example.com",
        "company_id": "example-company",
        "logo_size": "20",
        "qrcode_color": "#993366",
        "product_name": "name",
        "created_by": "ayush" 
        "is_active": boolean
    }
    