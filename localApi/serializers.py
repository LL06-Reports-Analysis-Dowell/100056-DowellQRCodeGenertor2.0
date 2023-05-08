from rest_framework import serializers
from .models import QrCode


class DoWellQrCodeSerializer(serializers.ModelSerializer):
    link = serializers.URLField(required=False)
    class Meta:
        model = QrCode
        fields = ['link', 'company_id', 'logo_size', 'qrcode_color']



class DoWellUpdateQrCodeSerializer(serializers.ModelSerializer):
    link = serializers.URLField(required=False)
    class Meta:
        model = QrCode
        fields = ['logo', 'qrcode', 'link', 'company_id', 'logo_size', 'qrcode_color', 'product_name',   
                    'created_by', 'is_active']


class DoWellDetailQrCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = QrCode
        fields = '__all__'


