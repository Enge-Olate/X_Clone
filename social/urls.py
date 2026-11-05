from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets.social_viewset import FollowViewSet

router = DefaultRouter()
router.register('follow', FollowViewSet, basename='follow')
urlpatterns = [
    path('', include(router.urls)),
]