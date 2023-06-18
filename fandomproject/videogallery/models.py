from django.db import models

# Create your models here.
class Gallery(models.Model):
    title = models.CharField(max_length=20)
    image = models.ImageField()

    def __str__(self):

        return self.title
