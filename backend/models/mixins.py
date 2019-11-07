import uuid

from django.db import models
from django.conf import settings


class TimestampFieldsMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ContactMixin(models.Model):
    first_name = models.CharField(max_length=settings.MAX_LENGTH_NAME)
    middle_name = models.CharField(max_length=settings.MAX_LENGTH_NAME)
    last_name = models.CharField(max_length=settings.MAX_LENGTH_NAME)
    email = models.EmailField(unique=True, null=True, blank=True)
    contact_number = models.CharField(
        max_length=settings.MAX_LENGTH_CONTACT_NUMBER,
        null=True, blank=True
    )

    class Meta:
        abstract = True

    @property
    def full_name(self):
        if self.middle_name:
            return '%s %s. %s' % (self.first_name, self.middle_name[0], self.last_name)
        return '%s %s' % (self.first_name, self.last_name)


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
