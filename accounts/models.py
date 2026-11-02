from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from PIL import Image, UnidentifiedImageError


def validate_image_file(value):
    """Garante que o upload seja uma imagem real e não apenas um arquivo com extensão válida."""
    allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    FileExtensionValidator(allowed_extensions=allowed_extensions)(value)
    try:
        with Image.open(value) as img:
            img.verify()
    except (UnidentifiedImageError, OSError, ValueError):
        raise ValidationError('Envie uma imagem válida.')


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[validate_image_file],
    )
    following = models.ManyToManyField(
        'self',
        related_name='followers',
        blank=True,
        symmetrical=False,
    )

    def __str__(self):
        return f'Perfil de {self.user.username}'