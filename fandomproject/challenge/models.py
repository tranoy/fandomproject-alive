from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=20)
    video = models.FileField(upload_to="video/%y")

    def __str__(self):
        return self.title

