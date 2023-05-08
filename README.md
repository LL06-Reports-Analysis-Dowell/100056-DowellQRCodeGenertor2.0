# 100056-DowellQRCodeGenertor2.0

## Summary
This project involves the creation of QR codes through an API.
QR codes are two-dimensional barcodes that can store data such 
as URLs and other types of information.

To use this API, clients can send HTTP requests to create, retrieve, 
update, or delete QR codes. The API supports the creation of QR 
codes with various options such as custom colors, logos, and sizes.

Clients can create QR codes by providing a link, a logo image, a 
logo size, and a custom color. The API will return a base64-encoded 
image of the QR code that can be used in various contexts such as 
websites, printed materials, or mobile apps.

The API also supports updating and retrieving QR codes by their unique
 identifiers. Clients can update various properties of a QR code such 
 as the link, logo, size, and color. Clients can also retrieve the 
 details of a QR code by its identifier.

Overall, this API provides a convenient way for clients to generate, 
customize, and manage QR codes for their applications.



## Prerequisites

Before you begin, make sure you have the following software installed on your computer:
    .Python 3.7+
    
## Step 1: Setting up the Django project in your local machine.
    
    Clone project by running the following command in your terminal:
    git clone git@github.com:LL06-Reports-Analysis-Dowell/100056-DowellQRCodeGenertor2.0.git

## Step 2: Run the Project in your local environment.

    Get into the projects directory by running:
    cd /100056-DowellQRCodeGenertor2.0

    Create a virtual enviroment and activate it in the terminal using
    
    python3 -m venv venve
    source venve/bin/activate - linux
    

    Install the requirements
    pip install -r requirements.txt

    Run the project:
    python3 manage.py runserver

## API Documentation 
## Creating QRcodes:
    Endpoint: 
    POST: http://127.0.0.1:8000/api/dowell_codeqr/ (server) 
    POST: http://127.0.0.1:8000/api/codeqr/ (local)

    This endpoint is used to create a QR code. The data to be sent should 
    be in the form of a multipart/form-data with the following fields:

    qrcode_color: (optional) A string representing the hex color code to
    be used as the background color of the QR code. Defaults to black 
    if not provided.


    Response Example:

    If the QR code was created successfully, the API will respond 
    with a JSON object containing the following fields. The _id field
    will be generated automatically.
    {
        "_id": "6435567b0d7b968d221dda18",
        "logo": null,
        "qrcode": "base64_string",
        "link": null,
        "product_name": null,
        "created_by": "name",
        "qrcode_type: null,
        "logo_size": 20,
        "qrcode_color": "#009933",
        "description": null,
        "is_active": boolean
    }


## Fetching qrcode QRcodes:
    Endpoint: 
    POST http://127.0.0.1:8000/api/dowell_codeqr/?product_name=product_name (server) 
    POST: http://127.0.0.1:8000/api/codeqr/?product_name=product_name (local)
    
    This endpoint is used to fetch QR codes generated by the application.
    The endpoint takes a product name as a parameter in the request body. 
    Which when passed, only qrcodes with the same product name 
    will be returned. Otherwise it will return a list of all qrcodes.

    Sample Response
    
    {
        "response": {
            "isSuccess": true,
            "data": [
                {
                    "_id": "6435567b0d7b968d221dda18",
                    "link": "https://example.com/",
                    "logo": "base64_string",
                    "qrcode": "base64_string",
                    "qrcode_color: "#ff0000",
                    "created_by": "name",
                    "company_id": "string",
                    "qrcode_type: null,
                    "product_name": "internet",
                    "description": "example description"
                    "is_active": boolean
                }
        }   ]
    }
    



## Fetching a single Qrcode
        
    To fetch a single Qrcode, make a GET request to the appropriate
    endpoint with the Qrcode's ID as a parameter. For example, to
    fetch the Qrcode with ID "123", you would make a request to:
    
    http://127.0.0.1:8000/api/dowell_codeqrupdate/123 --server
    http://127.0.0.1:8000/api/codeqrupdate/123 --local
    
    The response will be a JSON object containing the 
    Qrcode data, including its ID, link, logo, qrcode image,
    logo size, qrcode color, product name, creation date, and status.

    Example Response
    
     {
        "response": {
            "_id": "123",
            "link": "https://example.com/",
            "logo": "base64_string",
            "qrcode": "base64_string",
            "qrcode_color: "#ff0000",
            "created_by": "name",
            "company_id": "string",
            "qrcode_type: "string",
            "product_name": "internet",
            "description": "example description"
            "is_active": boolean
        }
    }
    

## Updating the Qrcode:

    To update a Qrcode, make a PUT request to the appropriate
    endpoint with the ID of the Qrcode you want to update, and 
    include the fields that you want to update in the request body. 
    For example, to update the link and logo of a Qrcode with ID "1234", 
    you would make a PUT request to 
    
    http://127.0.0.1:8000/api/dowell_codeqrupdate/1234 --server
    http://127.0.0.1:8000/api/codeqrupdate/1234 --local
    

    The data to be sent should be in the form of a multipart/form-data 
    with the following fields:
        link(required): The URL link that the Qrcode points to.
        logo(optional): The logo of the company that the Qrcode represents.
        logo_size(optional): The size of the logo in the Qrcode.
        company_id(optional): The ID of the company that the Qrcode represents.
        qrcode_color(optional): The color of the Qrcode.
        product_name(oprtional): The name of the product associated with the Qrcode.
        created_by(optional): The user who created the Qrcode.
        description(optional): Description of the Qrcode.

    Example of a successfull response will be:
    
        {
            "response: {   
                "_id": "6435567b0d7b968d221dda18",
                "logo": "base64_encoded_logo_image",
                "qrcode": "base64_encoded_qrcode_image",
                "link": "https://example.com",
                "company_id": "example-company",
                "logo_size": "20",
                "qrcode_color": "#ff0000",
                "product_name": "name",
                "created_by": "ayush",
                "description": "example description" 
                "is_active": true
            }
        }
        
    When the qrcode id is not found the Response will be:

        {
            "error": "'1234' is not a valid ObjectId, it must be a
                12-byte input or a 24-character hex string"
        }
    




hash value for qr id --done
link --done
link for activate --it can function with update endpoint
name of qrcode --should be product name
description 
number of qr code -*can be added as a query parameter in the create endpoint
color --done
logo image --done
enable functionality of qr code ??
status --is_active done
type of qr code 
product name --done