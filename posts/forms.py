from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image','description','status', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 20}),
            'tags': forms.TextInput(attrs={'placeholder': 'Введите теги через Enter.'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Напишите комментарий...'}),
        }
        labels = {
            'text': ''
        }


# class TagForm(forms.ModelForm):
#     class Meta:
#         model = Tag
#         fields = ['name']