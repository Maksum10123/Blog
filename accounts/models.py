from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username

class Subscribe(models.Model):
    author = models.ForeignKey(Profile, related_name='follows', on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, related_name='followers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author', 'user')

    def __str__(self):
        return f"{self.author} follows {self.user}"