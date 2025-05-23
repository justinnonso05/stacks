from django.urls import path
from . import views
from .views import HomeView, CreatePostView, PostDetailView, MessageView, SearchResultView, UpdatePostView, DeletePostView



urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('welcome/', views.landing, name = 'welcome'),
    path('new-post/', CreatePostView.as_view(), name = 'create-post'),
    path('posts/<int:pk>/<str:username>/', PostDetailView.as_view(), name = 'post-detail'),
    path('posts/edit/<int:pk>/', UpdatePostView.as_view(), name = 'edit-post'),
    path('posts/delete/<int:pk>/', DeletePostView.as_view(), name = 'delete-post'),
    path('app/messages/', MessageView.as_view(), name = 'message'),
    path('app/search/', SearchResultView.as_view(), name = 'search'),
    path('app/notifications/', views.materials, name = 'notifications'),
    path('app/groups/', views.groups, name = 'groups'),
    path('announcements/', views.announcement, name = 'announcement'),
    path('like/<int:post_id>/', views.like_post, name = 'like-post'),
    path('liked-post/<int:post_id>/', views.liked_posts, name = 'liked-post'),
    path('send_bulk_email/', views.send_bulk_email_view, name='send_bulk_email'),
]