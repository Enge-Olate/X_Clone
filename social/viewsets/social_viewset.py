
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.models import Profile
from core.mixins import HTMXAuthRedirectMixin
from core.utils import wants_html


class FollowViewSet(HTMXAuthRedirectMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.select_related("user").all()
    lookup_field = "user__username"
    lookup_url_kwarg = "username"

    def create(self, request, username=None):
        target = self.get_object()
        if target == request.user.profile:
            return Response({"error": "Você não pode seguir a si mesmo."}, status=400)
        request.user.profile.following.add(target)
        return self._render_or_json(target, "following")

    def destroy(self, request, username=None):
        target = self.get_object()
        request.user.profile.following.remove(target)
        return self._render_or_json(target, "unfollowed")

    @action(detail=True, methods=["post"])
    def toggle(self, request, username=None):
        target = self.get_object()
        if target in request.user.profile.following.all():
            request.user.profile.following.remove(target)
        else:
            request.user.profile.following.add(target)
        return self._render_or_json(target, "toggled")

    def _render_or_json(self, target, status_text):
        following = target in self.request.user.profile.following.all()
        if wants_html(self.request):
            return render(
                self.request,
                "partials/follow_button.html",
                {"profile": target},
            )
        return Response({"status": status_text, "following": following})

