from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from backend.users.urls import url_patterns as USERS_URLS


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include([
        USERS_URLS,
    ]))
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
