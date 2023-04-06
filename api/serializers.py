from rest_framework import serializers

class DoWellQrCodeSerializer(serializers.Serializer):
    logo = serializers.SerializerMethodField()
    link = serializers.URLField(max_length=128,allow_null=False, allow_blank=False)
