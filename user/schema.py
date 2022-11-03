from rest_framework import serializers


class SignUpReqSchema(serializers.Serializer):
    email = serializers.CharField(max_length=50, allow_null=False)
    password = serializers.CharField(max_length=255, allow_null=False)
