
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone




class Post(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     title = models.CharField(max_length=100)
     image = models.ImageField(upload_to='posts/', null=True)
     content = models.TextField(null=True, blank=True)
     date_created = models.DateTimeField(default=timezone.now)
     likes = models.IntegerField(default=0)
     dislikes = models.IntegerField(default=0)

     def __str__(self):
         return f'{self.user.username}-Post'

     def get_absolute_url(self):
         return reverse('post-detail', args=[str(self.id)])
     

    
class Comment(models.Model):
     question = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)
     content = models.TextField(null=True, blank=True)
     date_created = models.DateTimeField(default=timezone.now)
     likes = models.IntegerField(default=0, null=True)
     dislikes = models.IntegerField(default=0, null=True) 

     def __str__(self) -> str:
         return '%s- %s' % (self.question.title, self.question.user)

# import uuid
# from django.contrib.auth import get_user_model
# from django.db import models
# from django.conf import settings

# User = get_user_model()

# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class CustomUser(AbstractUser):
    

#     def __str__(self):
#         return self.username

# class Post(models.Model):
#     id = models.UUIDField(primary_key=True,
#                           default=uuid.uuid4,
#                           editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     content = models.TextField(null=True, blank=True)
#     image = models.ImageField(upload_to='posts/', null=True)
#     posted_on = models.DateTimeField(auto_now_add=True)
#     likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
#                                    related_name="liked_posts",
#                                    blank=True)

#     class Meta:
#         ordering = ['-posted_on']

#     def number_of_likes(self):
#         return self.likes.count()

#     def __str__(self):
#         return f'{self.user.username}\'s post'

# class Comment(models.Model):
#     post = models.ForeignKey(Post,
#                              on_delete=models.CASCADE,
#                              related_name='post_comments')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     text = models.CharField(max_length=100)
#     posted_on = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-posted_on']

#     def __str__(self):
#         return f'{self.user.username}\'s comment'


