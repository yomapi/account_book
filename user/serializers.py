from rest_framework import serializers
from user.models import Token, User as CustomUser


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class TokenSerializers(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = "__all__"
