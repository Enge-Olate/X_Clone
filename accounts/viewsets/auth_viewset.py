from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from ..serializers import UserSerializer
from core.utils import wants_html

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        django_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        if wants_html(request):
            return redirect('feed')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET', 'POST'])
    def login(self, request):
        if request.method == "GET":
            return render(request, 'auth/login.html')

        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            django_login(request, user)
            if wants_html(request):
                return redirect('feed')
            return Response({"status": "logged_in"})
        erro = "Usuário ou senha inválidos."
        if wants_html(request):
            return render(request, "auth/login.html", {'error': erro}, status=401)
        return Response({"error": erro}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        django_logout(request)
        if wants_html(request):
            return redirect('login')
        return Response({"status": "logged_out"})
