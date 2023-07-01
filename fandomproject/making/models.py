from django.conf import settings
from django.db import models
from django.utils import timezone

def transformed_image_upload_path(instance, filename):
    return 'transformed_images/{}'.format(filename)

class TransformedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    style = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    post_image = models.ImageField(upload_to='post_images', blank=True, null=True)

    def __str__(self):
        return self.style

class TransformedLog(models.Model):
    nickname = models.CharField(max_length=255, default='')
    image_url = models.CharField(max_length=255, default='')
    date = models.DateTimeField(default=timezone.now)  # date 필드 추가

    def __str__(self):
        return self.nickname
