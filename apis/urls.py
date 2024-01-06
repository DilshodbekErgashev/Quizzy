from django.urls import path

from .views import *


urlpatterns =[
    path("posts", PostAPIView.as_view(), name='post-search'),
    path("posts/create",PostListCreateView.as_view()),
    path("posts/<int:pk>",PostDetailView.as_view()),
    path("comments/",CommentCreateView.as_view()),
    path('search/',SearchPostView.as_view()),
    path("comments/<int:pk>",CommentDetailView.as_view()),
   

     
]