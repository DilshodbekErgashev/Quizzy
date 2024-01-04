
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
import quizzy_app

class Post(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     title = models.CharField(max_length=100)
     image = models.ImageField(upload_to='posts/', null=True, blank=True)
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
     likes = models.IntegerField(default=0)
     dislikes = models.IntegerField(default=0)

     def __str__(self) -> str:
         return '%s- %s' % (self.question.title, self.question.user)

     def save(self, *args, **kwargs):
         super().save(*args, **kwargs)

class Search(models.Model):
    title = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='searches')

    def __str__(self):
        return self.title


class Chat(models.Model):
    to_message = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    from_message = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def get_chats(cls, from_user, to_user):
        return cls.objects.filter(quizzy_app(from_message=from_user, to_message=to_user) | quizzy_app(from_message=to_user, to_message=from_user))

    @classmethod
    def get_or_create_chat(cls, from_user, to_user):
        chat, created = cls.objects.get_or_create(from_message=from_user, to_message=to_user)
        if not created:
            chat, created = cls.objects.get_or_create(from_message=to_user, to_message=from_user)
        return chat, created
