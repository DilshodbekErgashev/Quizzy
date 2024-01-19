
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
     likes = models.PositiveBigIntegerField(null=True, default=0)
     dislikes = models.PositiveBigIntegerField(null=True, default=0)

     def __str__(self):
         return f'{self.user.username}-Post'

     def get_absolute_url(self):
         return reverse('post-detail', args=[str(self.id)])
     
class CommentManager(models.Manager):
    def get_queryset_for_post(self, post_id):
        return self.filter(post_id=post_id)

class Comment(models.Model):
     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")   
     content = models.TextField(null=True, blank=True)
     date_created = models.DateTimeField(default=timezone.now)
     likes = models.PositiveBigIntegerField(null=True, default=0)
     dislikes = models.PositiveBigIntegerField(null=True, default=0)

     objects = CommentManager()

     def __str__(self) -> str:
        return '%s - %s' % (self.post.title, self.post.user)
