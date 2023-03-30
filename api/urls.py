from django.urls import path
from api.views import *

urlpatterns = [
    path('dowell/',DoWellView.as_view()),
    path('qrcode_generate/', QrCodeView.as_view()),
]