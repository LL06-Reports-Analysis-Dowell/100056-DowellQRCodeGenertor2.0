from django.urls import path
from app.views import *
from app.test_views import *

urlpatterns = [
    # testing api endpoints
    path('test/server-status/', testServerStatus.as_view()),
    
    # production api endpoints
    path('server-status/', serverSTatus.as_view()),
]