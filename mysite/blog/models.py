from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(blank=True, max_length=200, default="")
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    url = models.CharField(blank=True, max_length=200, default="")

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments

    def get_tags(self):
        ret = ""
        for tag in self.tags.all():
            ret = ret +" "+ tag.tag
        return ret

    def get_main_image(self):
        ret = self.images.filter()
        if ret:
            return ret[0].url
        else:
            return ""

class Image(models.Model):
    post = models.ForeignKey('blog.Post', related_name='images')
    url = models.CharField(blank=True, max_length=200, default="")

    def __str__(self):
        return self.text

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(blank=True, max_length=50, default="")
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class Tag(models.Model):
    post = models.ForeignKey('blog.Post', related_name='tags')
    tag = models.CharField(blank=True, max_length=50, default="")

    def get_tag(self):
        return str(self.tag).replace("#","")