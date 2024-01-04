
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



