from rest_framework import serializers

class DoWellQrCodeSerializer(serializers.Serializer):
    logo = serializers.CharField(allow_null=True)
    product_name = serializers.CharField(max_length=128,allow_null=False, allow_blank=False)
    link = serializers.URLField(max_length=128,allow_null=False, allow_blank=False)
    company_id = serializers.CharField(max_length=128,allow_null=False, allow_blank=False)
    create_by = serializers.CharField(max_length=128,allow_null=False, allow_blank=False)



    # logo = serializers.ImageField(allow_null=True, allow_empty_file=False)
    #  logo = serializers.SerializerMethodField()
