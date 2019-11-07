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

    def __str__(self):
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
        return f'{self.profile}'


class Fee(models.Model):
    fee_type = models.CharField('Fee Type', max_length=1)
    date_issued = models.DateField('Date Issued')
    short_description = models.CharField(
        'Short Description',
        max_length=settings.MAX_LENGTH_SHORT_DESCRIPTION,
        blank=True, null=True
    )
    description = models.TextField()
    deadline = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    is_paid = models.BooleanField(default=False)

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    def __str__(self):
        paid = 'paid' if self.is_paid == True else 'not paid'
        return f'{self.driver} - {self.fee_type} - P{self.amount} - {paid}'
