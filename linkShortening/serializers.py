from rest_framework import serializers

class DoWellQrCodeSerializer(serializers.Serializer):
    logo = serializers.FileField(required=False, allow_null=True)
    qrcode_color = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    user_id = serializers.CharField(max_length=255, required=True, allow_null=False, allow_blank=False)
    company_id = serializers.CharField(max_length=255, required=True, allow_null=False, allow_blank=False)
    # quantity = serializers.CharField(allow_null=True, allow_blank=False, required=False)
    # logo_size = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    # created_by = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    # document_name = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    # description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    # is_active = serializers.BooleanField(required=False, allow_null=True, default=False)
    

class LinkSerializer(serializers.Serializer):
    link = serializers.URLField(required=True, allow_null=False)
    is_opened = serializers.BooleanField(default=False, allow_null=True)
    is_finalized = serializers.BooleanField(default=False)
    word = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    word2 = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    word3 = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)


class LinkTypeSerializer(DoWellQrCodeSerializer):
    links = LinkSerializer(many=True, required=True, allow_null=False)


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