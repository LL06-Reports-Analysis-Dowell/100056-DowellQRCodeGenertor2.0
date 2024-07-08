from django.urls import path
from .views import QRCodeAPIView, MasterQRCodeAPIView, CloneQRCodeAPIView, QRCodeDataAPIView, redirect_link,FindQRCodeAPIView,CreateQRCode

urlpatterns = [
    path('qrcodes/', QRCodeAPIView.as_view(), name='qrcode-list-create'),
    path('qrcodes/<str:qrcode_id>/', QRCodeAPIView.as_view(), name='qrcode-detail'),
    path('master-qrcodes/', MasterQRCodeAPIView.as_view(), name='master-qrcode-create'),
    path('activate-qr-code/<str:master_qr_code_id>/', MasterQRCodeAPIView.as_view(), name='activate-qr-code'),
    path('master-qrcodes/update/<str:master_qr_code_id>/', MasterQRCodeAPIView.as_view(), name='update-master-qr'),
    #path('clone-qrcode/', CloneQRCodeAPIView.as_view(), name='clone-qrcode'),
    path('redirect_link/<str:qrcode_id>/', redirect_link, name='qr_code_view'),
    path('qrcode-data/', QRCodeDataAPIView.as_view(), name='qrcode-data'),
    path('qrcode-data/<str:qrcode_id>/', QRCodeDataAPIView.as_view(), name='qrcode-data'),
    path('find-mastercode/', FindQRCodeAPIView.as_view(), name='qrcode-data'),
    path('create-mastercode/', CreateQRCode.as_view(), name='create-mastercode'),

]
