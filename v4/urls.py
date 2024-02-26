from django.urls import path
from .views import *

urlpatterns = [
    path('server-status/', serverStatus.as_view()),

    path('qr-code/', codeqr.as_view()),
    path('decrypt-qrcode/', DecryptQRCode.as_view(), name='decrypt_qrcode'),
    path('update-qr-code/<str:id>/', codeqrupdate.as_view()),
    path('inactive/', inactive, name="inactive"),
    path('activate-qr-code/<str:id>/', codeqractivate.as_view()),
]