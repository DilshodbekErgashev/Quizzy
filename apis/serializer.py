from rest_framework.serializers import  ModelSerializer
from rest_framework import  serializers
from quizzy_app.models import Post,Comment,Chat

class PostSerializer(ModelSerializer):
    user = serializers.CharField(read_only=True)
    class Meta:
        model= Post
        fields = ("title", "image", "user","content","likes","dislikes")
        
        
class CommentSerializer(ModelSerializer):
    class Meta:
        model= Comment
        fields= "__all__"
        
class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
        
from quizzy_app.models import Search

class SearchSerializer(ModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'