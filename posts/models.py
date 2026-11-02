from django.db import models
from django.conf import settings
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    content = models.TextField(
        max_length=280,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )   
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_posts',
        blank=True,
    )
    reposts = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='reposted_posts',
        blank=True,
    )
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Post de {self.author.username} - {self.created_at}"
    
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments' 
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    content = models.TextField(
        max_length=280,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )