from django.urls import path
from .views import (
    QRCodeListCreateView,
    QRCodeDetailView,
    QRCodeActivateView,
    QRCodeUpdateDataView
)

urlpatterns = [
    path('qrcodes/', QRCodeListCreateView.as_view(), name='qrcode-list-create'),
    path('qrcodes/<int:pk>/', QRCodeDetailView.as_view(), name='qrcode-detail'),
    path('qrcodes/<int:pk>/activate/', QRCodeActivateView.as_view(), name='qrcode-activate'),
    path('qrcodes/<int:pk>/update-data/', QRCodeUpdateDataView.as_view(), name='qrcode-update-data'),
]
