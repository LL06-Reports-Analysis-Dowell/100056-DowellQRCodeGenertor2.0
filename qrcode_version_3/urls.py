from django.urls import path
from app.views import *

urlpatterns = [
    path('server-status/', serverStatus.as_view()),

    path('qr-code/', codeqr.as_view()),
    path('update-qr-code/<str:id>/', codeqrupdate.as_view()),
]