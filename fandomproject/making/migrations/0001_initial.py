# Generated by Django 4.2.2 on 2023-06-28 05:19

from django.db import migrations, models
import making.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TransformedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to=making.models.transformed_image_upload_path)),
            ],
        ),
    ]
