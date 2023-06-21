from django.db import models

# Create your models here.

# class Category(models.Model):
#     name = models.CharField(max_length=100, null=False, blank=False)

#     def __str__(self):
#         return self.name
    
class Video(models.Model):
    title = models.CharField(max_length=200)
    video_key = models.CharField(max_length=12)

