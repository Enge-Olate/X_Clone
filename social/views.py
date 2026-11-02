from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.models import Profile
from django.shortcuts import get_object_or_404
# Create your views here.
class FollowViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def _get_target_profile(self, pk):
        return get_object_or_404(Profile, pk=pk)
    
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        target_profile = self._get_target_profile(pk)
        if request.user.profile == target_profile:
            return Response({'error': 'Você não pode seguir a si mesmo.'}, status=status.HTTP_400_BAD_REQUEST)  
        
        request.user.profile.following.add(target_profile)
        return Response({'status': 'seguindo'},status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        target_profile = self._get_target_profile(pk)
        
        request.user.profile.following.remove(target_profile)
        return Response({'status': 'deixou de seguir'},status=status.HTTP_200_OK)