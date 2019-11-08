from django.conf import settings

from rest_framework import serializers

from backend.users import models


class SignUpInitialValidation(serializers.Serializer):
    username = serializers.CharField(max_length=settings.MAX_LENGTH_USERNAME)
    password = serializers.CharField(max_length=settings.MAX_LENGTH_PASSWORD)
    confirm_password = serializers.CharField(
        max_length=settings.MAX_LENGTH_PASSWORD)

    def validate(self, attrs):
        # pylint: disable=no-member

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('Passwords do not match!')

        try:
            user = models.User.objects.get(username=attrs['username'])
        except models.User.DoesNotExist:
            return attrs

        if user:
            raise serializers.ValidationError('Username has been taken!')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=settings.MAX_LENGTH_USERNAME)
    password = serializers.CharField(max_length=settings.MAX_LENGTH_PASSWORD)
