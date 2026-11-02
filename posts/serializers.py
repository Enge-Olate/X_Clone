from rest_framework import serializers
from .models import Post, Comment
from accounts.serializers import ProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(source='author.profile', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(source='author.profile', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    reposts_count = serializers.IntegerField(source='reposts.count', read_only=True)
    is_liked= serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'updated_at', 'likes_count', 'reposts_count', 'comments', 'is_liked']
    
    def get_is_liked(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj.likes.filter(
            id = user.id
        ).exists()