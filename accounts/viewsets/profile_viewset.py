from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from ..serializers import ProfileSerializer
from ..models import Profile
from core.utils import wants_html
from core.mixins import HTMXAuthRedirectMixin


class ProfileViewSet(HTMXAuthRedirectMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'user_username'
    lookup_url_kwarg = 'username'

    def retrieve(self, request, *args, **kwargs):
        profile = self.get_object()
        if wants_html(request):
            return render(request, "profile/detail.html", {"profile": profile})
        return Response(self.get_serializer(profile).data)

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def follow(self, request, username=None):
        target = self.get_object()
        if target == request.user.profile:
            return Response({"error": "Você não pode seguir a si mesmo."}, status=400)
        request.user.profile.following.add(target)
        return self._render_or_json(target='following')

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def unfollow(self, request, username=None):
        target = self.get_object()
        request.user.profile.following.remove(target)
        return self._render_or_json(target='unfollowed')

    def _render_or_json(self, target, status_text):
        if wants_html(self.request):
            return render(self.request, "partial/follow_button.html", {"profile": target})
        return Response({"status": status_text, "following": target in self.request.user.profile.following.all()})
