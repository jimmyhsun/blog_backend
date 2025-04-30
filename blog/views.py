from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import PostService
from .serializers import PostSerializer, UserRegisterSerializer, LoginSerializer, RefreshTokenSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from blog.models import Post
from .permissions import IsAdminOrAuthorCanEdit

@extend_schema(
    request=LoginSerializer,
    summary="登入，拿到Token",
)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'token_type': 'Bearer',
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'expires_in': 15 * 60,
                    'user': {
                        'id': user.id,
                        'role': user.role
                    }
                })
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=RefreshTokenSerializer,
    summary="刷新Token",
)
class CustomTokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            refresh_token_str = serializer.validated_data['refresh']

            try:
                refresh_token = RefreshToken(refresh_token_str)
                access_token = refresh_token.access_token

                return Response({
                    'token_type': 'Bearer',
                    'access_token': str(access_token),
                    'refresh_token': str(refresh_token),
                    'expires_in': 15 * 60,  # 秒
                })
            except TokenError as e:
                return Response({'error': 'Invalid or expired refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=UserRegisterSerializer,
    summary="註冊帳號",
)
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=PostSerializer,
    summary="貼文",
)
class PostListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = PostService.list_posts()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = PostService.create_post(
                author=request.user,
                title=serializer.validated_data['title'],
                content=serializer.validated_data['content']
            )
            output_serializer = PostSerializer(post)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@extend_schema(
    request=PostSerializer,
    summary="單一貼文",
)
class PostRetrieveUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrAuthorCanEdit]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if post.author != request.user:
            return Response({'detail': 'You do not have permission to edit this post.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if post.author != request.user:
            return Response({'detail': 'You do not have permission to delete this post.'},
                            status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
