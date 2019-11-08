from django.contrib import admin

from backend.users import models


admin.site.register(models.User)
admin.site.register(models.Profile)
admin.site.register(models.License)
admin.site.register(models.Driver)
admin.site.register(models.Fee)
admin.site.register(models.Violation)
admin.site.register(models.Vehicle)
