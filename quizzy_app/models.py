
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_created = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name="customuser_set",
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="customuser_set",
        blank=True
    )

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'quizzy_app_customuser'

class Post(models.Model):
     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
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
