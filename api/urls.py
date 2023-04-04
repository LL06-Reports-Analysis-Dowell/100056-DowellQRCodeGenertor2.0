from django.urls import path
from api.views import *

urlpatterns = [
    path('do_well_qr_code/',DoWellQrCodeView.as_view()),
    path('test/',test.as_view()),
    path('test/<str:company_id>/',test.as_view()),
]