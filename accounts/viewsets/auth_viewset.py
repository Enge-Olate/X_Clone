from django.contrib.auth import authenticate, get_user_model, login as django_login, logout as django_logout
from django.shortcuts import redirect, render
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.utils import wants_html
from ..models import Profile
from ..serializers import UserSerializer

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Profile.objects.get_or_create(user=user)
        django_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        if wants_html(request):
            return redirect('feed-list')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET', 'POST'])
    def login(self, request):
        if request.method == 'GET':
            return render(request, 'auth/login.html')

        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            Profile.objects.get_or_create(user=user)
            django_login(request, user)
            if wants_html(request):
                return redirect('feed-list')
            return Response({'status': 'logged_in'})

        error = 'Usuário ou senha inválidos.'
        if wants_html(request):
            return render(request, 'auth/login.html', {'error': error}, status=401)
        return Response({'error': error}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        django_logout(request)
        if wants_html(request):
            return redirect('auth-login')
        return Response({'status': 'logged_out'})
