from django.db import models
from datetime import datetime
from django.conf import settings

# Create your models here.

## 준오님
# class Video(models.Model):
#     title = models.CharField(max_length=20)
#     video = models.FileField(upload_to="video/%y")

#     def __str__(self):
#         return self.title

class Video(models.Model):
    # title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='challenge_upload/', default=0)
    ref_id = models.IntegerField(default=0)
    
class Ref_Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    singer = models.CharField(max_length=10, default=None)
    video_file = models.FileField(upload_to='ref_video/', default=0)
    img = models.CharField(max_length=255,default=0)
    
class Score(models.Model):
    nickname = models.CharField(max_length=255)
    score = models.IntegerField()
    video_file = models.FileField(upload_to='output/', default = 0)
    ref_id = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)