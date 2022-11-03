from rest_framework import serializers


class BookCreateReq(serializers.Serializer):
    memo = serializers.CharField(max_length=1024)
    amount = serializers.IntegerField()
