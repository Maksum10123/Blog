from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path, include
from accounts.views import register_view, profile
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('register/', register_view, name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('profile/<int:user_id>', profile, name="profile"),
    path('subscription/<int:user_id>/', views.subscription, name='subscription'),
    path('profile/<int:user_id>/edit', views.edit_profile, name="editprofile"),
    path('promote/<int:user_id>', views.make_staff, name="staff"),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)