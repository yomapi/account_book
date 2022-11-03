from rest_framework import serializers
from account_book.models import BaseModel


class BaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        fields = "__all__"
