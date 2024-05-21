from rest_framework import serializers
from .models import QRCode, QRCodeClone, QRCodeVersion, MasterLink
class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = ['id', 'data', 'created_at', 'updated_at', 'is_active']

class QRCodeCloneSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCodeClone
        fields = ['id', 'original_qrcode', 'data', 'created_at']

class QRCodeVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCodeVersion
        fields = ['id', 'qrcode', 'data', 'version_number', 'created_at']

class MasterLinkSerializer(serializers.ModelSerializer):
    qrcodes = QRCodeSerializer(many=True, read_only=True)
    link = serializers.URLField(read_only=True)

    class Meta:
        model = MasterLink
        fields = ['id', 'name', 'qrcodes', 'link']