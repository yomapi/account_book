from rest_framework import serializers
from book.models import Book


class BookSerializers(serializers.ModelSerializer):
    def validate_amount(self, value: int):
        if value > 0:
            return value
        else:
            raise serializers.ValidationError("amout must be bigger than 0")

    class Meta:
        model = Book
        fields = "__all__"
