from rest_framework import serializers
from .models import QrCode


class DoWellQrCodeSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=False)
    link = serializers.URLField(required=False)
    class Meta:
        model = QrCode
        fields = ['logo', 'qrcode', 'link', 'company_id', 'logo_size', 'qrcode_color', 'is_active']


