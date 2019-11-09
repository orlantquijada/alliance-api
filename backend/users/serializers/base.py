from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from backend.users import models
from backend.utils import globals


class ProfileSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(
        format=globals.DATE_FORMAT, input_formats=(globals.DATE_FORMAT,))

    profile_pic = Base64ImageField(required=False)

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
        format=globals.DATE_FORMAT, input_formats=(globals.DATE_FORMAT,))
    date_of_expiry = serializers.DateField(
        format=globals.DATE_FORMAT, input_formats=(globals.DATE_FORMAT,))

    class Meta:
        model = models.License
        fields = (
            'id', 'date_issued', 'date_of_expiry', 'restriction_numbers',
            'condition_code', 'agency_code', 'license_number'
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('id', 'username')


class DriverSerializer(serializers.ModelSerializer):
    # pylint: disable=no-member

    user_id = serializers.PrimaryKeyRelatedField(
        source='user', queryset=models.User.objects.all())
    license_id = serializers.PrimaryKeyRelatedField(
        source='license', queryset=models.License.objects.all())
    profile_id = serializers.PrimaryKeyRelatedField(
        source='profile', queryset=models.Profile.objects.all())

    user = UserSerializer(read_only=True)
    profile = ProfileSerializer(read_only=True)
    license = LicenseSerializer(read_only=True)

    class Meta:
        model = models.Driver
        fields = ('id', 'user_id', 'license_id', 'profile_id',
                  'user', 'license', 'profile')


class ViolationSerializer(serializers.ModelSerializer):
    # pylint: disable=no-member

    datetime_issued = serializers.DateTimeField(
        format=globals.DATETIME_FORMAT, input_formats=(globals.DATETIME_FORMAT,))

    driver_id = serializers.PrimaryKeyRelatedField(
        source='driver', queryset=models.Driver.objects.all())
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = models.Violation
        fields = ('id', 'name', 'short_description', 'is_counted',
                  'description', 'datetime_issued', 'location', 'driver_id', 'driver')


class FeeSerializer(serializers.ModelSerializer):
    # pylint: disable=no-member

    deadline = serializers.DateField(
        format=globals.DATE_FORMAT, input_formats=(globals.DATE_FORMAT,)
    )

    driver_id = serializers.PrimaryKeyRelatedField(
        source='driver', queryset=models.Driver.objects.all())
    driver = DriverSerializer(read_only=True)
    violation_id = serializers.PrimaryKeyRelatedField(
        source='violation', queryset=models.Violation.objects.all())
    violation = ViolationSerializer(read_only=True)

    class Meta:
        model = models.Fee
        fields = (
            'id',  'driver_id', 'violation_id', 'deadline',
            'is_paid', 'amount', 'driver', 'violation',
        )


class VehicleSerializer(serializers.ModelSerializer):
    # pylint: disable=no-member

    driver_id = serializers.PrimaryKeyRelatedField(
        source='driver', queryset=models.Driver.objects.all())
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = models.Vehicle
        fields = ('id', 'driver_id', 'driver', 'make',
                  'model', 'year', 'plate_number', 'status_type')


class PartyInvolvedSerializer(serializers.ModelSerializer):
    # pylint: disable=no-member

    license_id = serializers.PrimaryKeyRelatedField(
        source='license', queryset=models.License.objects.all(), required=False)
    vehicle_id = serializers.PrimaryKeyRelatedField(
        source='vehicle', queryset=models.Vehicle.objects.all(), required=False)

    violation_id = serializers.PrimaryKeyRelatedField(
        source='violation', queryset=models.Violation.objects.all())

    license = LicenseSerializer(read_only=True, required=False)
    vehicle = VehicleSerializer(read_only=True, required=False)
    violation = ViolationSerializer(read_only=True)

    class Meta:
        model = models.PartyInvolved
        fields = ('id', 'license_id', 'vehicle_id', 'violation_id',
                  'license', 'vehicle', 'violation')


class NotificationSerializer(serializers.ModelSerializer):
    # pylint: disable=no-member

    driver_id = serializers.PrimaryKeyRelatedField(
        source='driver', queryset=models.Driver.objects.all())
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = models.Notification
        fields = ('id', 'driver_id', 'driver', 'is_viewed',
                  'description', 'notification_type')
