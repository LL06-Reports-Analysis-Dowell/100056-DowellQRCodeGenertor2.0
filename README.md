# 100056-DowellQRCodeGenertor2.0

## API Documentation 

created a post request method

created a Qrcode with the logo field

After generating the Qrcode it Convert the image to a base64-encoded string and save the datas to the database

## Creating a QR code using Python Django

In this ReadMe file, we will be creating a simple QR code generator using Python Django. 

## Prerequisites

Before you begin, make sure you have the following software installed on your computer:

    .Python 3.x
    .Django 3.x
    .qrcode library (can be installed using pip)

## Step 1: Setting up the Django project

Create a new Django project by running the following command in your terminal:

    *git clone git@github.com:LL06-Reports-Analysis-Dowell/100056-DowellQRCodeGenertor2.0.git

## Next, create a new Django app within the project:

    *cd /path/100056-DowellQRCodeGenertor2.0
    *python manage.py startapp qr_app

## Install the requirements

    *pip install djangorestframework
    *pip install django-cors-headers
    *pip install requests
    *mkvirtualenv a
    *source djangoenv/bin/activate
    *python3 -m venv djangoenv
## Create a new workspace in postman and do apost request

## Create a QRcode with a company id:

    company_id : "example-company"
    logo: "image.png"
    POST REQUEST : http://127.0.0.1:8000/api/codeqr/


## Update the Qrcode with Following Input Fields:

    link: "example.com"
    company_id: "example1company"
    Qrcode_color: #ff000
    logo: "image.png"
    PUT REQUEST: http://127.0.0.1:8000/api/codeqrupdate/<str:company_id>


## Fetch the QRcode using Company_id as Query parameter:

    GET REQUEST : http://127.0.0.1:8000/api/codeqr/?company_id=company_id