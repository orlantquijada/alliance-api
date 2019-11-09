from django.utils import timezone
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.conf import settings

from backend.models import mixins
from backend.users import choices, managers


class User(AbstractBaseUser, PermissionsMixin, mixins.TimestampFieldsMixin, mixins.UUIDMixin):
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    username = models.CharField(
        max_length=settings.MAX_LENGTH_USERNAME, unique=True)

    user_type = models.CharField(
        'User Type', max_length=1, choices=choices.USER_TYPES, default=choices.DRIVER)

    USERNAME_FIELD = 'username'

    objects = managers.UserManager()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f'{self.username}'


class Profile(mixins.ContactMixin):
    profile_pic = models.ImageField(
        'Profile Picture',
        upload_to='users/profile-pictures/',
        blank=True, null=True
    )
    sex = models.CharField(
        max_length=1,
        choices=choices.SEX,
        null=True, blank=True
    )
    address = models.CharField(
        max_length=settings.MAX_LENGTH_ADDRESS,
        null=True, blank=True
    )

    blood_type = models.CharField(
        'Blood Type', max_length=2, choices=choices.BLOOD_TYPES)
    eye_color = models.CharField(max_length=settings.MAX_LENGTH_EYE_COLOR)

    height = models.PositiveSmallIntegerField('Height (cm)')
    weight = models.PositiveSmallIntegerField('Weight (kg)')

    nationality = models.CharField(max_length=settings.MAX_LENGTH_NATIONALITY)
    birth_date = models.DateField('Birth Date')
    points = models.PositiveIntegerField(default=20)

    def __str__(self) -> str:
        return self.full_name

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.middle_name = self.middle_name.capitalize()
        self.last_name = self.last_name.capitalize()

        super().save(*args, **kwargs)


class License(models.Model):
    date_issued = models.DateField('Date Issued')
    date_of_expiry = models.DateField('Date of Expiry')

    restriction_numbers = models.CharField(
        'Restriction Numbers', max_length=settings.MAX_LENGTH_RESTRICTION_NUMBERS)
    condition_code = models.CharField(
        max_length=1, choices=choices.CONDITION_CODES, null=True, blank=True)
    agency_code = models.CharField(
        'Agency Code', max_length=settings.MAX_LENGTH_AGENCY_CODE)
    license_number = models.CharField(
        'License Number', max_length=settings.MAX_LENGTH_LICENSE_NUMBER)

    def __str__(self) -> str:
        return f'{self.license_number}'


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    license = models.OneToOneField(License, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.profile}'


class Violation(models.Model):
    name = models.CharField(max_length=settings.MAX_LENGTH_NAME)
    short_description = models.CharField(
        'Short Description',
        max_length=settings.MAX_LENGTH_SHORT_DESCRIPTION,
        blank=True, null=True
    )
    description = models.TextField()
    datetime_issued = models.DateTimeField(
        'Datetime Issued')
    location = models.CharField(max_length=settings.MAX_LENGTH_ADDRESS)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    is_counted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.datetime_issued}'


class Fee(models.Model):
    deadline = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    is_paid = models.BooleanField(default=False)

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    violation = models.ForeignKey(Violation, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'fees'

    def __str__(self) -> str:
        paid = 'paid' if self.is_paid else 'not paid'
        return f'{self.driver} - {self.violation.name} - P{self.amount} - {paid}'


class Vehicle(models.Model):
    make = models.CharField(max_length=settings.MAX_LENGTH_NAME)
    model = models.CharField(max_length=settings.MAX_LENGTH_NAME)
    year = models.PositiveIntegerField()
    plate_number = models.CharField(
        'Plate Number', max_length=settings.MAX_LENGTH_PLATE_NUMBER)

    status_type = models.CharField(
        max_length=2, choices=choices.STATUS_TYPES, default=choices.OK)

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'vehicles'

    def __str__(self) -> str:
        # pylint: disable=no-member

        return f'{self.make} - {self.model} - {self.year} - {self.driver.profile.full_name}'


class Notification(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    is_viewed = models.BooleanField(default=False)
    description = models.CharField(
        max_length=settings.MAX_LENGTH_SHORT_DESCRIPTION)
    notification_type = models.CharField(
        'Notification Type', max_length=1, choices=choices.STATUS_TYPES)

    class Meta:
        default_related_name = 'notifications'

    def __str__(self) -> str:
        # pylint: disable=no-member

        viewed = 'viewed' if self.is_viewed else 'not viewed'
        return f'{self.driver.profile.full_name} - {viewed}'


class PartyInvolved(models.Model):
    license = models.ForeignKey(
        License, on_delete=models.CASCADE, null=True, blank=True)
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, null=True, blank=True)

    involvement_description = models.CharField(
        'Involvement Description', max_length=settings.MAX_LENGTH_SHORT_DESCRIPTION)

    violation = models.ForeignKey(Violation, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'parties_involved'

    def __str__(self) -> str:
        # pylint: disable=no-member

        s = self.vehicle.plate_number if self.vehicle else self.license.license_number
        return f'{s} - {self.violation}'
