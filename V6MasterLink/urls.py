from django.urls import path
from .views import QRCodeAPIView, MasterQRCodeAPIView

urlpatterns = [
    path('qrcodes/', QRCodeAPIView.as_view(), name='qrcode-list-create'),
    path('qrcodes/<str:qrcode_id>/', QRCodeAPIView.as_view(), name='qrcode-detail'),
    path('master-qrcodes/', MasterQRCodeAPIView.as_view(), name='master-qrcode-create'),
    path('master-qrcodes/<str:master_qr_code_id>/', MasterQRCodeAPIView.as_view(), name='qrcode-detail'),
    path('activate-qr-code/<str:master_qr_code_id>/', MasterQRCodeAPIView.as_view(), name='activate-qr-code'),
    # path('clone-qrcode/<str:master_qr_code_id>/', CloneQRCodeAPIView.as_view(), name='clone-qrcode'),
]
