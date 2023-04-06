from rest_framework import serializers

class DoWellQrCodeSerializer(serializers.Serializer):
    logo = serializers.SerializerMethodField()
    # product_name = serializers.CharField(max_length=128,allow_null=False, allow_blank=False)
    link = serializers.URLField(max_length=128,allow_null=False, allow_blank=False)
    # company_id = serializers.CharField(max_length=128,allow_null=False, allow_blank=False)
    # create_by = serializers.CharField(max_length=128,allow_null=False, allow_blank=False)