from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from ..models import Post
from ..serializers import PostSerializer
from core.mixins import HTMXAuthRedirectMixin
from core.utils import wants_html

class FeedViewSet(HTMXAuthRedirectMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    
    def _get_followed_posts(self):
        followed = self.request.user.profile.following.all()
        return (Post.objects
            .filter(author__profile__in=followed)
            .select_related("author", "author__profile")
            .prefetch_related("likes", "reposts", "comments")
            .distinct())

    def list(self, request):
        posts = self._get_followed_posts()

        if wants_html(request):
            return render(request, "feed/home.html", {"posts": posts})

        serializer = self.get_serializer(
            posts, many=True, context={"request": request}
        )
        return Response(serializer.data)

