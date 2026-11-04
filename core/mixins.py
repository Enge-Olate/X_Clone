from django.shortcuts import redirect
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from .utils import wants_html


class HTMXAuthRedirectMixin:

    def handle_exception(self, exc):
        if isinstance(exc, (NotAuthenticated, PermissionDenied)) and wants_html(self.request):
            return redirect('login')
        return super().handle_exception(exc)