from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('register/', views.signup, name = 'signup'),
    path('<str:username>/profile/create/', CreateProfileView.as_view(), name = 'create-profile'),
    path('<str:username>/profile/edit/', EditProfileView.as_view(), name = 'edit-profile'),
    path('<str:username>/profile/', DetailProfileView.as_view(), name = 'user-profile'),
]