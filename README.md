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

## Create a view fuction

    import qrcode

    from django.http import HttpResponse


    def generate_qr(request, data):
        # create a QR code instance
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)

        # add data to the QR code
        qr.add_data(data)
        qr.make(fit=True)

        # create an image from the QR code
        img = qr.make_image(fill_color="black", back_color="white")

        # serve the image as an HTTP response
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return response

## Adding a URL pattern
    from django.urls import path
    from . import views

    urlpatterns = [
        path('qr/<str:data>/', views.generate_qr, name='generate_qr'),
    ]

## Run the Project

    *python manage.py runserver
