from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets.feed_viewset import FeedViewSet
from .viewsets.comment_viewset import CommentViewSet
from .viewsets.post_viewset import PostViewSet
router = DefaultRouter()
router.register("feed",FeedViewSet, basename='feed')
router.register("comments",CommentViewSet, basename='comments')
router.register("post",PostViewSet, basename='post')

urlpatterns=[
    path('', include(router.urls)),
]