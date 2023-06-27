from django.db import models

def transformed_image_upload_path(instance, filename):
    return 'transformed_images/{}'.format(filename)

class TransformedImage(models.Model):
    style = models.CharField(max_length=255)
    image = models.ImageField(upload_to=transformed_image_upload_path)

    def __str__(self):
        return self.style