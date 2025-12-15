from idlelib.query import Query

from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from taggit.models import Tag
from django.db.models import Q
from .models import Post, Like, Profile, Comment
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy


def home(request):
    posts = Post.objects.filter(status='published').order_by('-created_at')
    if request.user.is_authenticated:
        for post in posts:
            # Создаем временное поле прямо в объекте post
            post.user_liked = Like.objects.filter(post=post, user=request.user).exists()
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
            form.save_m2m()
            return redirect("home")
    return render(request, 'main/createpost.html', {'form': form})

def search_by_tag(request):
    query = request.GET.get("q")
    result = []
    all_tags = Tag.objects.all()
    if query:
        result = (
            Post.objects.filter(tags__name__icontains=query).distinct().order_by('-created_at')
        )

    return render(request, 'main/search.html', {'result': result, 'query': query, 'all_tags': all_tags})

@login_required
def search_users(request):
    query = request.GET.get("q")
    result = []
    if query:
        result = (
            Profile.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))
        )
    context = {'result': result, 'query': query}
    return render(request, 'main/user_search.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm()
    comments = Comment.objects.filter(post=post).order_by('-created')

    if not request.user.is_authenticated:
        user_liked = False
    else:
        user_liked = Like.objects.filter(post=post, user=request.user).exists()
    return render(request, 'main/post_detail.html', {'post': post, 'user_liked': user_liked, 'form': form, 'comments': comments})

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    like = Like.objects.filter(post=post, user=user).first()
    if like:
        like.delete()
    else:
        Like.objects.create(post=post, user=user)

    next_page = request.META.get('HTTP_REFERER')

    if next_page:
        return HttpResponseRedirect(next_page)

    return redirect('post_detail', post_id=post.id)

@login_required
def publish_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.post = post
            comment.save()
            form.save_m2m()
            return redirect('post_detail', post_id=post.id)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('home')

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        form.fields['tags'].disabled = True
        if form.is_valid():
            form.save()
            return redirect("post_detail", post_id=post.id)
    else:
        form = PostForm(instance=post)
        form.fields['tags'].disabled = True

    return render(request, 'main/post_edit.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('home')

    if request.method == "POST":
        post.delete()
        return redirect('home')

    return render(request, 'main/post_confirm_delete.html', {'post': post})