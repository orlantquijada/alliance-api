from rest_framework import serializers

from backend.users import serializers as user_serializers


class FeeQuerySerializer(serializers.Serializer):
    is_paid = serializers.NullBooleanField(required=False)
    driver_id = serializers.IntegerField(required=False)


class VehicleQuerySerializer(serializers.Serializer):
    driver_id = serializers.IntegerField(required=False)
