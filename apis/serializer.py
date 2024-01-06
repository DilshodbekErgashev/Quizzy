from rest_framework.serializers import  ModelSerializer
from rest_framework import  serializers
from quizzy_app.models import Post,Comment

class PostSerializer(ModelSerializer):
    user = serializers.CharField(read_only=True)
    class Meta:
        model= Post
        fields = ("title", "image", "user","content","likes","dislikes")
        
        
class CommentSerializer(ModelSerializer):
    class Meta:
        model= Comment
        fields= "__all__"
        
        extra_kwargs = {
            "likes": {"read_only": True},
            "dislikes": {"read_only": True},
            "date_created": {"read_only": True},
        }
        
class SearchPostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"