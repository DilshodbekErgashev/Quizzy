# Generated by Django 5.0 on 2024-01-18 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzy_app', '0008_rename_user_post_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='author',
            new_name='user',
        ),
    ]
