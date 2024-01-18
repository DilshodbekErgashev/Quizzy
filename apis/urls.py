from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView,TokenBlacklistView
from .views import *




urlpatterns =[
    path('register/', CustomUserRegistrationView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'), 
    path("posts", PostAPIView.as_view(), name='post-search'),
    path("posts/create",PostListCreateView.as_view()),
    path("posts/<int:pk>",PostDetailView.as_view()),
    path("like/", like),
    path('comments/',CommentCreateView.as_view()),
    path("comments/<int:pk>",CommentDetailView.as_view()),
    # path('post/<int:post_id>/comments', CreateReadCommentView.as_view({'post': 'create', 'get': 'list'})),
    path('search/',SearchPostView.as_view()),
]