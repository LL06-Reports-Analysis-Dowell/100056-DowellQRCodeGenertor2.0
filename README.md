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

## Passing the request json in the postman under port http://127.0.0.1:8000/api/codeqr/

    {
   "link": "https://www.netflix.com/ke/",
   "product_name": "internet",
   "logo": "logo.png"
   "create_by": "Iregi",
   "company_id": "3344uy"
   }

## Example of response
    {
    "Response": {
        "link": "https://www.netflix.com/ke/",
        "logo": "iVBORw0KGgoAAAANSUhEUgAAAFIAAABSCAIAAABIThTMAAARn0lEQVR4nO1ceXAc1Zn/fe919/SMRppDt2RrfUiyMdjYYbETg7mXMySLKVKBQM4lriKwCTmAQCqbra1NTIpdsoHKLlkgoUJIIBwhOCHHmiWcNob4tpEPYZ2WLGlGoxmNZqb7vW//aFkCWSPNyAe1Mb8a/fPU/fr79XvvO99rYmacfBDvtwDvDz6gfTLhA9onE4z34Zk8+ncYBDrRIhx/2gwwe2aSiCA8kkcQ1e+95"......
    },
    "qrcode": "iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAAD6UlEQVR4nO3bsWskZRjH8e+TmdxGEGYkVxyo3CIcnIIQUbCcEQtLsfAaLfIfKHY23oudlVfbuCCClWgjVsdMd4XCFmK9BxYnnjoDEnPZmTwW72xym3k3+ya42YjvW2yybz55+c2+".....


