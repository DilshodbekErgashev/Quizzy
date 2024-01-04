from django.urls import path, re_path

from .views import *
from apis import views

urlpatterns =[
    path("posts", PostAPIView.as_view(), name='post-search'),
    path("posts/create",PostListCreateView.as_view()),
    path("posts/<int:pk>",PostDetailView.as_view()),
    path("comments/",CommentCreateView.as_view()),
    path("search/",SearchListAPIView.as_view()),
    path("comments/<int:pk>",CommentDetailView.as_view()),
    re_path(r'^chat/$', views.ChatList.as_view(), name='chat-get-list'),
    re_path(r'^chat/(?P<from_id>.+)&(?P<to_id>.+)/$', views.ChatList.as_view(), name='chat-list'),

     
]