from django.urls import path
from api.views import *

urlpatterns = [
    path('test_database/',test_database.as_view()),
    path('test_database/<str:company_id>/',test_database.as_view()),
]