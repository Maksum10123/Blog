from django import template
from django.contrib.auth import get_user_model

User = get_user_model()
register = template.Library()

@register.filter
def follow_to(author, user):
    return author.follows.filter(user=user).exists()