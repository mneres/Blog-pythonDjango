from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved=True)

class Image(models.Model):
    post = models.ForeignKey('blog.Post', related_name='images')
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.text

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text