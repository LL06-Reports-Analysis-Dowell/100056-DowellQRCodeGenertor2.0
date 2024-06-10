from django.urls import path
from .views import *
from v4 import views

urlpatterns = [
    path('server-status/', serverStatus.as_view()),

    path('qr-code/', codeqr.as_view()),
    path('decrypt-qrcode/', DecryptQRCode.as_view(), name='decrypt_qrcode'),
    path('decrypt/<str:qrcode_id>/', decryptQrCode.as_view(), name='decrypt_qrcode'),
    path('update-qr-code/<str:id>/', codeqrupdate.as_view()),
    path('inactive/', inactive, name="inactive"),
    path('activate-qr-code/<str:id>/', codeqractivate.as_view()),
    path('<str:qrcode_id>/', views.redirect_link, name='qr_code_view'),
    path('delete/<created_by>/', decryptQrCode.as_view(), name='delete_by_creator'),
    path('qrcode-Report-data/', QRCodeReportAPIView.as_view(), name='qrcode-data'),
    path('qrcode-Report-data/<str:qrcode_id>/', QRCodeReportAPIView.as_view(), name='qrcode-data'),
]