from django.contrib import admin
from django.urls import path, include

from backend.users.urls import url_patterns as USERS_URLS

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include([
        USERS_URLS,
    ]))
]
