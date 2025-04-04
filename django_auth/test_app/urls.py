from django.urls import path
from .views import register_user, create_post, get_posts
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('create-post/', create_post, name='create-post'),
    path('get-post/', get_posts, name='get-post'),
]