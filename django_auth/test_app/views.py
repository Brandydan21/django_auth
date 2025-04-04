from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import Post
from rest_framework.permissions import IsAuthenticated

# Register a new user 
@api_view(['POST'])
@permission_classes([AllowAny])  # Publicly accessible
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(
        username=username,
        email=email,
        password=make_password(password),  # important!
    )

    return Response({'message': 'User registered successfully', 'user_id': user.id}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    """
    Create a post. Only authenticated users can create a post.
    """
    if request.method == 'POST':
        # Manually get the data from request
        title = request.data.get('title')
        content = request.data.get('content')

        if not title or not content:
            return JsonResponse({'error': 'Title and Content are required fields'}, status=400)

        try:
            # Manually create a Post object
            post = Post.objects.create(
                user=request.user,
                title=title,
                content=content
            )

            # Return the created post as a response
            response_data = {
                'id': post.id,
                'user': post.user.id,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at
            }
            return JsonResponse(response_data, status=201)
        
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts(request):
    """
    Get a list of posts. Only authenticated users can view posts.
    """
    posts = Post.objects.all()  # You can filter this if you want to show posts specific to the logged-in user

    post_list = []
    for post in posts:
        post_data = {
            'id': post.id,
            'user': post.user.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at
        }
        post_list.append(post_data)

    return JsonResponse(post_list, safe=False) 