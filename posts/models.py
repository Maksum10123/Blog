from django.db import models
from accounts.models import Profile

from taggit.managers import TaggableManager

# class Tag(models.Model):
#     name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    )


    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author')
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = TaggableManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author} posted"



class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, related_name='liked_posts', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')


    def __str__(self):
        return f"{self.user} liked post {self.post.id}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, related_name='comments', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.user} comment {self.post.id}"