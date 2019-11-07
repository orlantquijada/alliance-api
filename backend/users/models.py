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
        'User Type', max_length=1, choices=choices.USER_TYPES)

    USERNAME_FIELD = 'username'

    objects = managers.UserManager()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.username}'


class Profile(mixins.ContactMixin):
    profile_pic = models.ImageField(
        'Profile Picture',
        upload_to='users/',
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
    nationality = models.CharField(
        max_length=settings.MAX_LENGTH_NATIONALITY
    )

    height = models.PositiveSmallIntegerField()
    weight = models.PositiveSmallIntegerField()

    birth_date = models.DateField('Birth Date')
    points = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.full_name


class License(models.Model):
    date_issued = models.DateField('Date Issued')
    date_of_expiry = models.DateField('Date of Expiry')

    restriction_numbers = models.CharField(
        'Restriction Numbers', max_length=settings.MAX_LENGTH_RESTRICTION_NUMBERS)
    condition_code = models.CharField(
        max_length=1, choices=choices.CONDITION_CODES)
    agency_code = models.CharField(
        'Agency Code', max_length=settings.MAX_LENGTH_AGENCY_CODE)
    license_number = models.CharField(
        'License Number', max_length=settings.MAX_LENGTH_LICENSE_NUMBER)

    def __str__(self):
        return f'{self.license_number}'


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    license = models.OneToOneField(License, on_delete=models.PROTECT)

    def __str__(self):
        return self.profile
