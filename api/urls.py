from django.urls import path
from api.views import *

urlpatterns = [
    path('codeqr/',codeqr.as_view()),
]