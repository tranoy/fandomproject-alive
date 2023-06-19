from django.db import models

# Create your models here.
class Gallery(models.Model):
    title = models.CharField(max_length=20)
    image = models.ImageField()
    user_id = models.TextField(default='') # 글쓴이
    like_count = models.IntegerField(default=0) # 좋아요 수

    def __str__(self):

        return self.title
