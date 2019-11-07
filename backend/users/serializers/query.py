from rest_framework import serializers


class FeeQuerySerializer(serializers.Serializer):
    is_paid = serializers.NullBooleanField(required=False)
