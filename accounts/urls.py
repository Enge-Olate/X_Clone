from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets.profile_viewset import ProfileViewSet
from .viewsets.auth_viewset import AuthViewSet
router = DefaultRouter()
router.register('auth', AuthViewSet, basename='auth')
router.register('profiles', ProfileViewSet , basename='profile')

urlpatterns=[
    path('', include(router.urls)),
]