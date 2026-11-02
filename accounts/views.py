from rest_framework import (
    generics,
    viewsets,
    permissions
)
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Profile
from .serializers import ProfileSerializer, UserSerializer
# Create your views here.

User = get_user_model()

class ResgisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permissions_classes = [permissions.AllowAny]
    
    def get_object(self):
        return self.request.user.profile

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
