from rest_framework import serializers
from .models import QrCode

# class DoWellQrCodeSerializer(serializers.Serializer):
#     logo = serializers.CharField(allow_null=True)
#     product_name = serializers.CharField(max_length=128,allow_null=False, allow_blank=False)
#     link = serializers.URLField(max_length=128,allow_null=False, allow_blank=False)
#     company_id = serializers.CharField(max_length=128,allow_null=False, allow_blank=False)
#     create_by = serializers.CharField(max_length=128,allow_null=False, allow_blank=False)
#     logo_size = serializers.CharField(max_length=128,allow_null=False, allow_blank=False, required=False)
#     logo_color = serializers.CharField(max_length=128,allow_null=False, allow_blank=False, required=False)

#     qrcode_color = serializers.CharField(max_length=128,allow_null=False, allow_blank=False, required=False)

    # logo = serializers.ImageField(allow_null=True, allow_empty_file=False)
    #  logo = serializers.SerializerMethodField()

class DoWellQrCodeSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=False)
    class Meta:
        model = QrCode
        fields = ['logo', 'qrcode', 'link', 'company_id', 'logo_size', 'qrcode_color', 'is_active']


