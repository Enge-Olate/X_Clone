from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# Create your views here.
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_profile = self.request.user.profile
        followed_profiles = user_profile.following.all()
        return Post.objects.filter(author__profile__in=followed_profiles).distinct()

class PostViewSet(viewsets.ModelViewSet): 
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return Response({'status': 'descurtido'})
        post.likes.add(request.user)
        return Response({'status': 'curtido'})
    
    @action(detail=True, methods=['post'])
    def repost(self, request, pk=None):
        post = self.get_object()
        if request.user in post.reposts.all():
            post.reposts.remove(request.user)
            return Response({'status': 'descompartilhado'})
        post.reposts.add(request.user)
        return Response({'status': 'compartilhado'})
    

class CommentViewSet(viewsets.ModelViewSet):
    serialezer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Comment.objects.filter(post_id = self.kwargs.get('post_pk'))\
            if 'post_pk' in self.kwargs else Comment.objects.all()
    
    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['post_pk'])        
        serializer.save(author= self.request.user, post=post)
    