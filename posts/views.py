from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, TagForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import Post, Like


def home(request):
    posts = Post.objects.filter(status='published').order_by('-created_at')
    return render(request, 'main/home.html', {'posts':posts})

@login_required
def create_post(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home")
    return render(request, 'main/createpost.html', {'form': form})

@staff_member_required
def create_tag(request):
    form = TagForm()
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=True)
            tag.save()
            return redirect("home")
    return render(request, 'main/createtag.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not request.user.is_authenticated:
        user_liked = False
    else:
        user_liked = Like.objects.filter(post=post, user=request.user).exists()
    return render(request, 'main/post_detail.html', {'post': post, 'user_liked': user_liked})

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    like = Like.objects.filter(post=post, user=user).first()
    if like:
        like.delete()
    else:
        Like.objects.create(post=post, user=user)

    return redirect('post_detail', post_id=post.id)