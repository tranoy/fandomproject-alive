# Generated by Django 4.2.2 on 2023-06-28 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0004_ref_video_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='text',
            field=models.TextField(default='-'),
        ),
    ]
