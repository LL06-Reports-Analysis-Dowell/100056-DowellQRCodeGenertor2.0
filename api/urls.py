from django.urls import path
from api.views import *

urlpatterns = [
    path('codeqr/',codeqr.as_view()),
    path('fetchdata/<str:company_id>',fetchdata.as_view()),
    path('getdata/<str:product_name>',getdata.as_view()),
]




# 3344uy