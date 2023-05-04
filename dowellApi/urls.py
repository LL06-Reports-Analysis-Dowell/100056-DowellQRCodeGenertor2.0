from django.urls import path
from .views import codeqr, codeqrupdate

urlpatterns = [
    path('dowell_codeqr/', codeqr.as_view()),
    path('dowell_codeqrupdate/<str:id>', codeqrupdate.as_view()),
]


