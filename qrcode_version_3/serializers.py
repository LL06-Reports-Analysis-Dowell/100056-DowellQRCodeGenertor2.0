from rest_framework import serializers

class DoWellQrCodeSerializer(serializers.Serializer):
    TYPE_CHOICES = (
        ('Product', 'Product'),
        ('Vcard', 'Vcard'),
        ('Link', 'Link')
    )
    qrcode_type = serializers.ChoiceField(choices=TYPE_CHOICES)
    quantity = serializers.CharField(allow_null=True, allow_blank=False, required=False)
    logo = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    # link = serializers.URLField(max_length=255, required=False, allow_null=True, allow_blank=True)
    company_id = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    logo_size = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    qrcode_color = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    created_by = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    is_active = serializers.BooleanField(required=False, allow_null=True, default=False)


class AddressSerializer(serializers.Serializer):
    street_address = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    city = serializers.CharField(max_length=255)
    state = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    zip_code = serializers.IntegerField(required=False, allow_null=True)
    country = serializers.CharField(max_length=255)
    
class ProductTypeSerializer(DoWellQrCodeSerializer):
    title = serializers.CharField(max_length=255)
    product_name = serializers.CharField(max_length=255)
    website = serializers.CharField(max_length=255)


class LinkSerializer(serializers.Serializer):
    link = serializers.URLField(required=True, allow_null=False)
    is_opened = serializers.BooleanField(default=False, allow_null=True)
    is_finalized = serializers.BooleanField(default=False)
   

class LinkTypeSerializer(DoWellQrCodeSerializer):
    links = LinkSerializer(many=True, required=True, allow_null=False)


class VcardSerializer(DoWellQrCodeSerializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=255)
    address = AddressSerializer()

class DoWellUpdateQrCodeSerializer(serializers.Serializer):
    qrcode_id=serializers.CharField(required=False, allow_null=True, allow_blank=True)

    logo_url = serializers.CharField(allow_null=True)
    qrcode_image_url = serializers.CharField(allow_null=True)
    
    link = serializers.URLField(max_length=255)
    company_id = serializers.CharField(max_length=255, allow_null=False, allow_blank=False)
    logo_size = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    qrcode_color = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    product_name = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    created_by = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    is_active = serializers.BooleanField(default=True)



class LinkFinalizeSerializer(serializers.Serializer):
    is_finalized = serializers.BooleanField(default=False)