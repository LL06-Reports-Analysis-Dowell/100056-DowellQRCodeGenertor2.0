from rest_framework import serializers


class DoWellQrCodeSerializer(serializers.Serializer):
    logo = serializers.CharField(allow_null=True)
    link = serializers.URLField(max_length=128, required=False, allow_null=True, allow_blank=True)
    company_id = serializers.CharField(max_length=128, allow_null=False, allow_blank=False)
    logo_size = serializers.CharField(max_length=128, required=False, allow_null=True, allow_blank=True)
    qrcode_color = serializers.CharField(max_length=128, required=False, allow_null=True, allow_blank=True)
    product_name = serializers.CharField(max_length=128, required=False, allow_null=True, allow_blank=True)
    created_by = serializers.CharField(max_length=128, required=False, allow_null=True, allow_blank=True)
    is_active = serializers.BooleanField(required=False, allow_null=True, default=False)


class DoWellUpdateQrCodeSerializer(serializers.Serializer):
    logo = serializers.CharField(allow_null=True)
    link = serializers.URLField(max_length=128)
    company_id = serializers.CharField(max_length=128, allow_null=False, allow_blank=False)
    logo_size = serializers.CharField(max_length=128, required=False, allow_null=True, allow_blank=True)
    qrcode_color = serializers.CharField(max_length=128, required=False, allow_null=True, allow_blank=True)
    product_name = serializers.CharField(max_length=128, required=False, allow_null=True, allow_blank=True)
    created_by = serializers.CharField(max_length=128, required=False, allow_null=True, allow_blank=True)
    is_active = serializers.BooleanField(default=True)