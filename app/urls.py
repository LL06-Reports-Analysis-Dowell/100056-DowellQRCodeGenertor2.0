from django.urls import path
from app.views import *

urlpatterns = [
    path('server-status/', serverStatus.as_view()),
    path('create-qr-code/', createQrCode.as_view()),
    path('create-qr-code/<str:name>/', createQrCode.as_view()),
]