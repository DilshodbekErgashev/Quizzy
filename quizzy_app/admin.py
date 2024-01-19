from django.contrib import admin

from quizzy_app.models import CustomUser, Post,Comment

admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Comment)