from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    image = models.ImageField(upload_to='blog/images/user_images', blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name
    
class Blog(models.Model):
    title = models.CharField(max_length=80)
    summary = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/images/blog_images', blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.title
