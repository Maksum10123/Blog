from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from posts import views

urlpatterns = [
    path('', views.home, name="home"),
    path('create/', views.create_post, name="create_post"),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('create/tag', views.create_tag, name="create_tag"),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
