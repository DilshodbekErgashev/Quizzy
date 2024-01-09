from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', CustomUserViewSet)


urlpatterns =[
    path('register/', CustomUserRegistrationView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'), 
    path("posts", PostAPIView.as_view(), name='post-search'),
    path("posts/create",PostListCreateView.as_view()),
    path("posts/<int:pk>",PostDetailView.as_view()),
    path("comments/",CommentCreateView.as_view()),

]