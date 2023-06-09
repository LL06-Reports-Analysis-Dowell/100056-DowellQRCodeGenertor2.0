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
git clone `https://github.com/LL06-Reports-Analysis-Dowell/100056-DowellQRCodeGenertor2.0.git`

## Step 2: Run the Project in your local environment.

- Get into the projects directory by running:
cd /100056-DowellQRCodeGenertor2.0

- Create a virtual enviroment and activate it in the terminal using

- python3 -m venv venve
source venve/bin/activate - linux


- Install the requirements
pip install -r requirements.txt

- Run the project:
python3 manage.py runserver

## API Documentation 

### API Endpoints

- Base URL: `https://100099.pythonanywhere.com/api/v1/`


| HTTP Verbs | Endpoints                      | Action                                               |
|------------|--------------------------------|------------------------------------------------------|
| POST       | qr-code/                      | To Create Qrcode by passing the company_id and quantity         |
| GET        | qr-code/                      | To Get All Qrcode Created.                           |
| GET        | update-qr-code/:id/           | To retrieve the Qrcode Created by the a company_id   |
| PUT        | update-qr-code/:id/ .         | To Update the qr_code with data.                     |


##  Endpoints Definition(Request - Response):

#### Create QrCode
POST: `/qr-code/`

Request Body

```json
{
    "company_id": "<company_id>",
    "quantity": "2",
    "qrcode_type": "Link"
}
```

Note: 
This endpoint is used to create a QR code. The data to be sent should 
be in the form of a multipart/form-data:
The quantity field will determine the number of qrcodes created.
The qrcode_type will have multiple choices. i.e Vcard, Product etc. Each of
them will have different properties. 
To get the properties send the payload as it is and the response will show
the properties which are suppossed to be input.
e.g If you pass the qrcode_type as "Link" as shown above the response will be 
as shown below, indicating that it requires a link property.

```json
{
    "link": [
        "This field may not be null."
    ]
}
```



Response - 200 

Note : If the QR code was created successfully, the API will respond 
with a JSON object containing the following fields.

```json
    {
        "response": "<quantity> QR codes created successfully."
    }
```

GET: `/qr-code/:id/`

Note : This endpoint is used to get the QR code. The data to be sent should
be in the form of a multipart/form-data with the following fields:
company_id: (optional) A string representing the id of the company
to be used to get the QR code. Defaults to the logged in user if not
provided.
Response - 200 
```json
{
    "response": {
        "qrcode_id": "2982427012418900461",
        "qrcode_image_url": "http://67.217.61.253/media/QrCodes/qrcode_1686291776.jpg",
        "logo_url": "http://67.217.61.253/media/QrCodes/logo.png",
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
#### Update Method for the Qr_code

PUT: `/update-qr-code/:id`

Request Body
```json
{
    "company_id": "129492388099ew03239661",
    "qrcode_image_url": "http://67.217.61.253/media/QrCodes/qrcode_1686291776.jpg",
    "logo_url": "http://67.217.61.253/media/QrCodes/logo.png",
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
Response - 200 
```json
{
    "response": {
        "qrcode_image_url": "http://67.217.61.253/media/QrCodes/qrcode_1686291776.jpg",
        "logo_url": "http://67.217.61.253/media/QrCodes/logo.png",
        "logo_size": 20,
        "qrcode_color": "#000000",
        "link": "https://stackoverflow.com/questions/22282760/filenotfounderror-errno-2-no-such-file-or-directory",
        "company_id": "Doo....it well",
        "product_name": "internet",
        "created_by": "Iregi",
        "description": "This is a qrcode for dowell",
        "is_active": true
    }
}
```

#### Fetching a single Qrcode

GET : `/update-qr-code/:id/`

Note : The response will be a JSON object containing the 
Qrcode data, including its ID, link, logo, qrcode image,
logo size, qrcode color, product name, creation date, and status.

Response - 200
```json
{
"response": [
    {
        "_id": "645ce86ffab34b4c2eee7f6106",
        "qrcode_id": "1294923880we9903239661",
        "qrcode_image_url": "http://67.217.61.253/media/QrCodes/qrcode_1686291776.jpg",
        "company_id": "Dowell",
        "created_by": null,
        "is_active": true,
        "link": "https://stackoverflow.com/questions/22282760/filenotfounderror-errno-2-no-such-file-or-directory",
        "logo_size": 20,
        "logo_url": "http://67.217.61.253/media/QrCodes/logo.png",
        "product_name": "internet",
        "qrcode_color": "#000000"
    }
]
}
```

### Technologies Used

- [Python](https://nodejs.org/) is a programming language that lets you work more quickly and integrate your systems
  more effectively.
- [Storage] ()
- [Django](https://www.djangoproject.com/) is a high-level Python web framework that encourages rapid development and
  clean, pragmatic design.
- [Django Rest Framework](https://www.django-rest-framework.org/) Django REST framework is a powerful and flexible
  toolkit for building Web APIs.
- [MongoDB](https://www.mongodb.com/) is a free open source NOSQL document database with scalability and flexibility.
  Data are stored in flexible JSON-like documents.

### License

This project is available for use under
the [Apache](https://github.com/LL06-Reports-Analysis-Dowell/100056-DowellQRCodeGenertor2.0/blob/main/LICENSE) License.

