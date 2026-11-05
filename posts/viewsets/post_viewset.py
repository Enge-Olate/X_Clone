from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Post, Comment
from ..serializers import PostSerializer, CommentSerializer
from core.mixins import HTMXAuthRedirectMixin
from core.utils import wants_html

class PostViewSet(HTMXAuthRedirectMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def create_post(self, request, *args, **kwargs):
        if request.htmx:
            content = (request.data.get("content")or "").strip()
            if not content:
                return Response({"error": "Conteúdo vazio."}, status=400)
            post = Post.objects.create(author = request.user, content=content)
            return render(request, "partials/post_card.html", {"post":post})

        return super().create_post(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        if wants_html(request):
            return render(request, "posts/detail.html", {"post":post})
        return Response(self.get_serializer(post).data)
    
    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        post.refresh_from_db()
        
        if wants_html(request):
            return render(request, "partials/like_button.html", {"post":post})
        return Response({
            "liked":request.user in post.likes.all(),
            "likes_count":post.likes.count(),
        })
        
    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def respost(self, request, pk=None):
        post = self.get_object()
        if request.user in post.reposts.all():
            post.reposts.remove(request.user)
        else:
            post.reposts.add(request.user)
        post.refresh_from_db()
        
        if wants_html(request):
            return render(request, "partials/post_card.html", {"post":post})
        return Response(
            {
                "reposted": request.user in post.reports.all(),
                "repost_count": post.reposts.count(),
            }
        )
        
    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def comment(self, request, pk= None):
        post = self.get_object()
        content = (request.data.get("content") or "").strip()
        if not content:
            return Response({"error": "Comentário vazio"}, status = 400)
        
        comment = Comment.objects.create(
            post = post, 
            author = request.user, 
            content = content
        )
        
        if wants_html(request):
            return render(
                request,
                "partials/comment.html",
                {"comment":comment}
            )
        return Response(CommentSerializer(comment).data, status=201)
        