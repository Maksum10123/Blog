from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image','description','status', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 20}),
            'tags': forms.TextInput(attrs={'placeholder': 'Введите теги через Enter.'}),
        }

# class TagForm(forms.ModelForm):
#     class Meta:
#         model = Tag
#         fields = ['name']