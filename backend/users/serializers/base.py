from rest_framework import serializers

from backend.users import models
from backend.utils import globals


class ProfileSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(
        format=globals.DATE_FORMAT, input_formats=(globals.DATE_FORMAT,))

    class Meta:
        model = models.Profile
        fields = (
            'id', 'first_name', 'middle_name', 'last_name', 'email',
            'contact_number', 'sex', 'profile_pic', 'address',
            'blood_type', 'eye_color', 'height', 'weight', 'nationality',
            'birth_date', 'points'
        )


class LicenseSerializer(serializers.ModelSerializer):
    date_issued = serializers.DateField(
        format=globals.DATE_FORMAT, input_formats=(globals.DATE_FORMAT,)
    )
    date_of_expiry = serializers.DateField(
        format=globals.DATE_FORMAT, input_formats=(globals.DATE_FORMAT,)
    )

    class Meta:
        model = models.License
        fields = (
            'id', 'date_issued', 'date_of_expiry', 'restriction_numbers',
            'condition_code', 'agency_code', 'license_number'
        )


class DriverSerializer(serializers.ModelSerializer):
    # pylint: disable=no-member

    license_id = serializers.PrimaryKeyRelatedField(
        source='license', queryset=models.License.objects.all())
    profile_id = serializers.PrimaryKeyRelatedField(
        source='profile', queryset=models.Profile.objects.all())

    profile = ProfileSerializer(read_only=True)
    license = LicenseSerializer(read_only=True)

    class Meta:
        model = models.Driver
        fields = ('id', 'license_id', 'profile_id', 'license', 'profile')


class FeeSerializer(serializers.ModelSerializer):
    # pylint: disable=no-member

    date_issued = serializers.DateField(
        format=globals.DATE_FORMAT, input_formats=(globals.DATE_FORMAT,))
    deadline = serializers.DateField(
        format=globals.DATE_FORMAT, input_formats=(globals.DATE_FORMAT,)
    )

    driver_id = serializers.PrimaryKeyRelatedField(
        source='driver', queryset=models.Driver.objects.all())
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = models.Fee
        fields = (
            'id',  'driver_id', 'fee_type', 'date_issued', 'deadline', 'description',
            'short_description', 'is_paid', 'amount', 'driver'
        )
