import telebot
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from accounts import models
from posts.models import Post


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

@user_passes_test(lambda u: u.is_superuser)
def make_staff(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(models.Profile, pk=user_id)
        user.is_staff = True
        user.save()
    return redirect('profile', user_id=user_id)

@login_required
def profile(request, user_id):
    user = get_object_or_404(models.Profile, pk=user_id)
    posts = Post.objects.filter(author=user,status='published')
    return render(request, 'accounts/profile.html', {"profile": user, "posts": posts})

@login_required
def subscription(request, user_id):
    profile_user = get_object_or_404(models.Profile, pk=user_id)

    if profile_user == request.user:
        return redirect('profile', pk=user_id)

    subscribe, created = models.Subscribe.objects.get_or_create(author=request.user, user=profile_user)
    if not created:
        subscribe.delete()
    return redirect('profile', user_id=user_id)

@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(models.Profile, pk=user_id)
    if user != request.user:
        return redirect('profile', user_id=user_id)
    if request.method == "POST":
        user.username = request.POST.get("username")
        user.bio = request.POST.get("bio")
        uploaded_avatar = request.FILES.get("avatar")
        if uploaded_avatar:
            user.avatar = uploaded_avatar
        user.save()
        return redirect("profile", user_id=user_id)
    return render(request, 'accounts/editprofile.html', {"profile": user})

@login_required
def start_telegram_auth(request):
    token = request.user.generate_token()
    bot_name = "AuthMebotblogbot"
    link = f"https://t.me/{bot_name}?start={token}"
    return redirect(link)

def finish_telegram_auth(request, token, chat_id):
    try:
        profile = models.Profile.objects.get(tg_auth_token=token)
        profile.telegram_id = chat_id
        profile.tg_auth_token = ""
        profile.save()
        messages.success(request, "Телеграм успешно привязан")
    except models.Profile.DoesNotExist:
        messages.error(request, "Неверный токен")
    return redirect("home")



