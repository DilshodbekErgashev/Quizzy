from rest_framework.serializers import  ModelSerializer
from rest_framework import  serializers

from quizzy_app.models import CustomUser, Post,Comment

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email',  'password', 'confirm_password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Пароли не совпадают")

        user = CustomUser.objects.create_user(**validated_data, password=password)
        return user
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()

            if user:
                if user.check_password(password):
                    if not user.is_active:
                        raise serializers.ValidationError('User account is disabled.')
                    return {'user': user}
                else:
                    raise serializers.ValidationError('Unable to log in with provided credentials.')
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')
    
from quizzy_app.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    post_id = serializers.CharField(read_only=True)
    class Meta:
        model = Comment
        fields= "__all__"

    extra_kwargs = {
        "likes": {"read_only": True},
        "dislikes": {"read_only": True},
        "date_created": {"read_only": True},
    }

    def create(self, validated_data):
        post_id = validated_data.get('post')
        if post_id is not None:
            validated_data['post'] = post_id
        comment = Comment.objects.create(**validated_data)
        return comment
    




class PostSerializer(ModelSerializer):
    user = serializers.CharField(read_only=True)
    # comments = CommentSerializer(many=True)

    class Meta:
        model= Post
        fields = ["id", "title", "image", "user", "content", "likes", "dislikes"]

    
    def create(self, validated_data):
        validated_data["user"] = CustomUser.objects.get(id=self.context["request"].user.id)
        return super().create(validated_data)
    
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     post_obj = instance
    #     comments = post_obj.comments.all()
    #     data["comments"] = comments
    #     return data
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        post_obj = instance
        comments = post_obj.comments.all()
        comment_serializer = CommentSerializer(comments, many=True)
        data["comments"] = comment_serializer.data
        return data


    
class SearchPostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

