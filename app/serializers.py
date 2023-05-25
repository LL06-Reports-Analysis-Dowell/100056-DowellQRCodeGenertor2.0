from rest_framework import serializers
class DoWellQrCodeSerializer(serializers.Serializer):
    TYPE_CHOICES = (
        ('Product', 'Product'),
    )
    qrcode_type = serializers.ChoiceField(choices=TYPE_CHOICES)
    quantity = serializers.CharField(allow_null=True, allow_blank=False, required=False)
    logo = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    link = serializers.URLField(max_length=128, required=False, allow_null=True, allow_blank=True)
    company_id = serializers.CharField(max_length=128, required=False, allow_null=True, allow_blank=True)
    logo_size = serializers.CharField(max_length=128, required=False, allow_null=True, allow_blank=True)
    qrcode_color = serializers.CharField(max_length=128, required=False, allow_null=True, allow_blank=True)
    created_by = serializers.CharField(max_length=128, required=False, allow_null=True, allow_blank=True)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    is_active = serializers.BooleanField(required=False, allow_null=True, default=False)



class ProductTypeSerializer(DoWellQrCodeSerializer):
    title = serializers.CharField(max_length=128)
    product_name = serializers.CharField(max_length=128)
    website = serializers.CharField(max_length=128)

class DoWellUpdateQrCodeSerializer(serializers.Serializer):
    qrcode_id=serializers.CharField(required=False, allow_null=True, allow_blank=True)

    logo_url = serializers.CharField(allow_null=True)
    qrcode_image_url = serializers.CharField(allow_null=True)
    
    link = serializers.URLField(max_length=128)
    company_id = serializers.CharField(max_length=128, allow_null=False, allow_blank=False)
    logo_size = serializers.CharField(max_length=128, required=False, allow_null=True, allow_blank=True)
    qrcode_color = serializers.CharField(max_length=128, required=False, allow_null=True, allow_blank=True)
    product_name = serializers.CharField(max_length=128, required=False, allow_null=True, allow_blank=True)
    created_by = serializers.CharField(max_length=128, required=False, allow_null=True, allow_blank=True)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    is_active = serializers.BooleanField(default=True)