
from django.shortcuts import get_object_or_404
from requests import Response
from .serializer import  PostSerializer, CommentSerializer, SearchPostSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .permissions import IsOwnerOrAdmin, CanCreatePostOrComment, CanLikePostOrComment
from rest_framework.views import APIView
from quizzy_app.models import  Post,Comment
from django.db.models import Q
from rest_framework.permissions import AllowAny


class PostAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [CanCreatePostOrComment]

    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrAdmin]

class CommentCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CanCreatePostOrComment]



class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrAdmin]

class LikeView(APIView):
    permission_classes = [CanLikePostOrComment]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.likes += 1
        post.save()
        return Response(status=status.HTTP_200_OK)


class SearchPostView(generics.ListAPIView):
    queryset = Post.objects.all().order_by("likes")
    serializer_class = SearchPostSerializer
    
    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query is not None:
            return Post.objects.filter(title__icontains=query, )
        
        return None