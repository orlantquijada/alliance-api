from django.urls import path, include

from rest_framework import routers

from backend.users import views


ROUTER = routers.DefaultRouter()

ROUTER.register('profiles', views.ProfileViewSet)
ROUTER.register('drivers', views.DriverViewSet)
ROUTER.register('licenses', views.LicenseViewSet)
ROUTER.register('fees', views.FeeViewSet)
ROUTER.register('users', views.UserViewSet)
ROUTER.register('violations', views.ViolationViewSet)
ROUTER.register('vehicles', views.VehicleViewSet)

url_patterns = path('', include(ROUTER.urls))
