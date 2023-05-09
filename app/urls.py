from django.urls import path
from app.views import *

urlpatterns = [
    path('server-status/', serverSTatus.as_view()),
]