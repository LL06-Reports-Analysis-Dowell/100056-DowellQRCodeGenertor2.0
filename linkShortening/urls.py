from django.urls import path
from .views import *

urlpatterns = [
    path('server-status/', serverStatus.as_view()),

    path('api/v4/qr-code/', codeqr.as_view()),
    path('api/v4/update-qr-code/<str:id>', codeqrupdate.as_view()),

    path('api/v4/get-links/', getLinks, name="get_links"),
    path('<str:word>/<str:word2>/<str:word3>', Links.as_view(), name="master_link"),
]