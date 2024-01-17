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


class CommentCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    
    
from rest_framework import viewsets

# class CreateReadCommentView (viewsets.ModelViewSet):
#     serializer_class = CommentSerializer
#     permission_classes = [AllowAny]
#     queryset = Comment.objects.all()

#     def perform_create(self, serializer):
#         post = Post.objects.get(id=self.kwargs.get('post_id')) 
#         serializer.save(question=post)


#     def get_queryset(self): 
#          post_id = self.kwargs.get('post_id') 
#          return super().get_queryset().filter(post_id=post_id)
# from rest_framework import status
# class BoardViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.exclude(deleted=True)
#     serializer_class = PostSerializer
#     permission_classes = [IsOwnerOrReadOnly]

#     def destroy(self, request: Request, *args, **kwargs) -> Response:
#         board = self.get_object()
#         if not board.deleted:
#             board.deleted = True
#             board.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response(status=status.HTTP_400_BAD_REQUEST)

#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return PostSerializer

#         return super().get_serializer_class()

    # @action(detail=True, methods=['get', 'post', 'delete'], serializer_class=CommentSerializer)
    # def comments(self, request, pk=None):
    #     if self.request.method == 'GET':
    #         board = self.get_object()
    #         comments = board.comment_set.all()
    #         serializer = CommentSerializer(comments, many=True)

    #         return Response(serializer.data)

        # if self.request.method == 'POST':
        #     board = self.get_object()
        #     serializer = CommentSerializer(data=request.data)
        #     if serializer.is_valid():
        #         user = serializer.data['user']
        #         text = serializer.data['text']
        #         Comment.objects.create(board=board, user=user, text=text)

        #         return Response(status=status.HTTP_201_CREATED)

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