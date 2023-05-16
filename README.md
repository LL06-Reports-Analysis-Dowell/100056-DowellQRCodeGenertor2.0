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

### API Endpoints

- Base URL: `https://100099.pythonanywhere.com/api/v1/`


| HTTP Verbs | Endpoints                                   | Action                                                                     |
| ---------- | ------------------------------------------- | ---------------------------------------------------------------------------|


| POST       | /qr-code/                                   | To create Qrcode.                                                          | 




| GET        | /qr-code/                                   | To Get All Qrcode Created.                                                 |


| GET        | /update-qr-code/<id>/                       | To retrieve the Qrcode Created by passing the query parameter company_id   |


| PUT        | /update-qr-code/<id>/                       | To Update the qr_code with data.                                           |



## Creating QRcodes:
    Endpoint: 
    POST: https://100099.pythonanywhere.com/api/v1/qr-code/ (server) 

    Request Body

    ```
    {
        "company_id": "129492388099ew03239661",
    }
    ```

    This endpoint is used to create a QR code. The data to be sent should 
    be in the form of a multipart/form-data with the following fields:

    qrcode_color: (optional) A string representing the hex color code to
    be used as the background color of the QR code. Defaults to black 
    if not provided.


    Response Example: (200)

    If the QR code was created successfully, the API will respond 
    with a JSON object containing the following fields. The _id field
    will be generated automatically.

```Response Body

    {
    "response": {
        "qrcode_id": "2982427012418900461",
        "qrcode_image_url": "http://res.cloudinary.com/din7lejen/image/upload/v1684225075/kefhu4k2rmkreh8bqeo7.png",
        "logo_url": null,
        "logo_size": 20,
        "qrcode_color": "#000000",
        "link": null,
        "company_id": "Doo....it well",
        "product_name": null,
        "created_by": null,
        "description": null,
        "is_active": false
    }
}

## Get Method for the Qr_code
    Endpoint:
    GET: https://100099.pythonanywhere.com/api/v1/qr-code/{qrcode_id} (server)
    Request Body
    ```
    {
        "company_id": "129492388099ew03239661",
        }
        ```
        This endpoint is used to get the QR code. The data to be sent should
        be in the form of a multipart/form-data with the following fields:
        company_id: (optional) A string representing the id of the company
        to be used to get the QR code. Defaults to the logged in user if not
        provided.
        Response Example: (200)
        ```
        {
            "response": {
                "qrcode_id": "2982427012418900461",
                "qrcode_image_url": "http://res.cloudinary.com/din7lejen/image/upload/v1684225075/kefhu4k2rmkreh8bqeo7.png",
                "logo_url": null,
                "logo_size": 20,
                "qrcode_color": "#000000",
                "link": null,
                "company_id": "Doo....it well",
                "product_name": null,
                "created_by": null,
                "description": null,
                "is_active": false
                }
                }
                ```
                ### Delete Method for the Qr_code
                Endpoint:
                DELETE: https://100099.pythonanywhere.com/api/v1/qr-code/{qrcode_id} (server)
                Request Body
                ```
                {
                    "company_id": "129492388099ew03239661",
                    }
                    ```
                    This endpoint is used to delete the QR code. The data to be
                    sent should be in the form of a multipart/form-data with the
                    following fields:
                    company_id: (optional) A string representing the id of the
                    company to be used to delete the QR code. Defaults to the
                    logged in user if not provided.
                    Response Example: (200)
                    ```
                    {
                        "response": {
                            "qrcode_id": "2982427012418900461",
                            "qrcode_image_url": "http://res.cloudinary.com/din7lejen/image/upload/v1684225075/kefhu4k2rmkreh8bqeo7.png",
                            "logo_url": null,
                            "logo_size": 20,
                            "qrcode_color": "#000000",
                            "link": null,
                            "company_id": "Doo....it well",
                            "product_name": null,
                            "created_by": null,
                            "description": null,
                            "is_active": false
                            }
                            }
                            ```
                            ### Update Method for the Qr_code
                            Endpoint:
                            PUT: https://100099.pythonanywhere.com/api/v1/qr-code/{qrcode_id} (server)
                            Request Body
                            ```
                            {
                                "company_id": "129492388099ew03239661",
                                "qrcode_image_url": "http://res.cloudinary.com/din7lejen/image/upload/v1684225075/kefhu4k2rmkreh8bqeo7.png",
                                "logo_url": null,
                                "logo_size": 20,
                                "qrcode_color": "#000000",
                                "link": null,
                                "company_id": "Doo....it well",
                                "product_name": null,
                                "created_by": null,
                                "description": null,
                                "is_active": false
                                }
                                ```
                                ### Update Method for the Qr_code
                                Endpoint:
                                PUT: https://100099.pythonanywhere.com/api/v1/qr-code/{qrcode_id} (client)
                                Request Body
                                ```
                                {
                                    "company_id": "129492388099ew03239661",
                                    "qrcode_image_url": "http://res.cloudinary.com/din7lejen/image/upload/v1684225075/kefhu4k2rmkreh8bqeo7.png",
                                    "logo_url": null,
                                    "logo_size": 20,
                                    "qrcode_color": "#000000",
                                    "link": null,
                                    "company_id": "Doo....it well",
                                    "product_name": null,
                                    "created_by": null,
                                    "description": null,
                                    "is_active": false
                                    }
                                    ```
                                    ### Delete Method for the Qr_code
                                    Endpoint:
                                    DELETE: https://100099.pythonanywhere.com/api/v1/qr-code/{qrcode_id} (server)
                                    ```
                                    ```
                                    ### Delete Method for the Qr_code
                                    Endpoint:
                                    DELETE: https://100099.pythonanywhere.com/api/v1/qr-code/{qrcode_id} (client)
                                    ```
                                    ### List Method for the Qr_code
                                    Endpoint:
                                    GET: https://100099.pythonanywhere.com/api/v1/qr-code (server)
                                    ```
                                    ```
                                    ### List Method for the Qr_code
                                    Endpoint:
                                    GET: https://100099.pythonanywhere.com/api/v1/qr-code (client)
                                    ```
                                 

## Fetching qrcode QRcodes:
    Endpoint: 
    POST https://100099.pythonanywhere.com/api/v1/apiupdate-qr-code//?product_name=product_name (server) (*Fetching by query param)
    POST https://100099.pythonanywhere.com/api/v1/apiupdate-qr-code/ (server) (*Fetch All qrcodes)

    
    
    This endpoint is used to fetch QR codes generated by the application.
    The endpoint takes a product name as a parameter in the request body. 
    Which when passed, only qrcodes with the same product name 
    will be returned. Otherwise it will return a list of all qrcodes.

    Sample Response
    Status 200
    
    {
        "response": {
            "isSuccess": true,
            "data": [
                {
                    "_id": "6435567b0d7b968d221dda18",
                    "link": "https://example.com/",
                    "logo_url": "http://res.cloudinary.com/din7lejen/image/upload/v1683810fee476/dh6tnzs8tykwffzdoz1l.png",
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
    GET : https://100099.pythonanywhere.com/api/v1/update-qr-code/12949238809we903239661/
    
    The response will be a JSON object containing the 
    Qrcode data, including its ID, link, logo, qrcode image,
    logo size, qrcode color, product name, creation date, and status.

    Example Response
    
    {
        "response": [
            {
                "_id": "645ce86ffab34b4c2eee7f6106",
                "qrcode_id": "1294923880we9903239661",
                "qrcode_image_url": "https://res.cloudinary.com/din7lejen/image/upload/v1683810476/vtapr9x9bl6oj2m1wm7r.png",
                "company_id": "Dowell",
                "created_by": null,
                "is_active": true,
                "link": "https://stackoverflow.com/questions/22282760/filenotfounderror-errno-2-no-such-file-or-directory",
                "logo_size": 20,
                "logo_url": "http://res.cloudinary.com/din7lejen/image/upload/v1683810476/dh6tnzs8tykwffzdoz1l.png",
                "product_name": "internet",
                "qrcode_color": "#000000"
            }
        ]
    }
    

## Updating the Qrcode:

    To update a Qrcode, make a PUT request to the appropriate
    endpoint with the ID of the Qrcode you want to update, and 
    include the fields that you want to update in the request body. 
    For example, to update the link and logo of a Qrcode with ID "1234", 
    you would make a PUT request to 
    ## Endpoint
    PUT: https://100099.pythonanywhere.com/api/v1/update-qr-code/12949238ddc809903239661/

    Request Body

        {   
            "response": {
                "qrcode_id": "2982427012418900461",
                "qrcode_image_url": "http://res.cloudinary.com/din7lejen/image/upload/v1684225075/kefhu4k2rmkreh8bqeo7.png",
                "logo_url": null,
                "logo_size": 20,
                "qrcode_color": "#000000",
                "link": null,
                "company_id": "Doo....it well",
                "product_name": null,
                "created_by": null,
                "description": null,
                "is_active": false
            }
        }
    
    

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
            "response": {
                "link": "https://stackoverflow.com/questions/22282760/filenotfounderror-errno-2-no-such-file-or-directory",
                "logo_url": "http://res.cloudinary.com/din7lejen/image/upload/v1683810476/dh6tnzs8tykwffzdoz1l.png",
                "logo_size": 20,
                "company_id": "Dowell",
                "qrcode_color": "#000000",
                "product_name": "internet",
                "created_by": null,
                "qrcode_image_url": "https://res.cloudinary.com/din7lejen/image/upload/v16838ddd10476/vtapr9xdc9bl6oj2m1wm7r.png",
                "is_active": true
            }
        }
        
    When the qrcode id is not found the Response will be:

        {
            "error": "'1234' is not a valid ObjectId, it must be a
                12-byte input or a 24-character hex string"
        }
    


### Technologies Used

- [Python](https://nodejs.org/) is a programming language that lets you work more quickly and integrate your systems
  more effectively.
- [Django](https://www.djangoproject.com/) is a high-level Python web framework that encourages rapid development and
  clean, pragmatic design.
- [Django Rest Framework](https://www.django-rest-framework.org/) Django REST framework is a powerful and flexible
  toolkit for building Web APIs.
- [MongoDB](https://www.mongodb.com/) is a free open source NOSQL document database with scalability and flexibility.
  Data are stored in flexible JSON-like documents.

### License

This project is available for use under
the [Apache](https://github.com/LL06-Reports-Analysis-Dowell/100056-DowellQRCodeGenertor2.0/blob/main/LICENSE) License.

```

```

```

```