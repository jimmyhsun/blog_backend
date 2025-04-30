from django.urls import path
from .views import LoginView, PostListCreateView, RegisterView, CustomTokenRefreshView, PostRetrieveUpdateView

urlpatterns = [
    path('login', LoginView.as_view()),   # 登入
    path('token/refresh', CustomTokenRefreshView.as_view()),  # 刷新Token
    path('register', RegisterView.as_view()),  # 注册
    path('posts', PostListCreateView.as_view()),  # 貼文
    path('posts/<int:pk>', PostRetrieveUpdateView.as_view(), name='post_retrieve_update'),
]