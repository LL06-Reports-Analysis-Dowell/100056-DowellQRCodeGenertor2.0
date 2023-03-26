from rest_framework import serializers

class testDatabases(serializers.Serializer):
    name = serializers.CharField(max_length=128,allow_null=False, allow_blank=False)
    description = serializers.CharField(max_length=128,allow_null=False, allow_blank=False)
    company_id = serializers.CharField(max_length=128,allow_null=False, allow_blank=False)
