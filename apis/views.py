from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from requests import Request
from rest_framework.response import Response
from rest_framework import generics
from apis.permissions import IsOwnerOrReadOnly
from apis.serializer import CommentSerializer, CustomUserLoginSerializer, CustomUserSerializer, PostSerializer, SearchPostSerializer
from rest_framework.views import APIView
from quizzy_app.models import CustomUser, Post, Comment
from quizzy_app.models import  Post,Comment
from django.db.models import Q
from rest_framework.permissions import AllowAny 
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

from rest_framework_simplejwt.tokens import RefreshToken

class CustomUserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'message': 'Login successful', 'access_token': access_token})
        return Response(serializer.errors, status=400)
    
class PostAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Post.objects.all()
        query = self.request.GET.get('q', '')
        if query:
            return Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        
        return queryset
    
class CommentCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.get_queryset_for_post(post_id)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView): 
    serializer_class = CommentSerializer 
    permission_classes = [AllowAny]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.get_queryset_for_post(post_id)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs.get('comment_id'))
        return obj
        
class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.all()
        query = self.request.GET.get('q', '')
        if query:
            return Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        
        return queryset


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]



    
from rest_framework import viewsets



class SearchPostView(generics.ListAPIView):
    queryset = Post.objects.all().order_by("likes")
    serializer_class = SearchPostSerializer
    permission_classes=[AllowAny]
    
    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query is not None:
            return Post.objects.filter(title__icontains=query, )
        
        return None

@api_view(["POST"])
@permission_classes([AllowAny])
def like(request):
    post_id = request.data["post_id"]    
    action = request.data["action"] 
    
    obj = Post.objects.get(id=post_id)
    
    if action == 1:
        obj.likes += 1
    elif action == 0:
        obj.dislikes += 1
        
    obj.save()
    
    return Response({"data": "Like is added"}, status=201)


@api_view(["POST"])
@permission_classes([AllowAny]) 
def like_comment(request): 
    comment_id = request.data["comment_id"]
    action = request.data["action"]

    obj = Comment.objects.get(id=comment_id)

    if action == 1:
        obj.likes += 1
    elif action == 0:
        obj.dislikes += 1
    
    obj.save()

    return Response({"data": "Like is added for comment"}, status=201)