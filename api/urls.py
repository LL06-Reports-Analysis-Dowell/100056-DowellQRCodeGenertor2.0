from django.urls import path
from api.views import *

urlpatterns = [
    path('qr_code/',DOWELLQRCODE.as_view()),
]