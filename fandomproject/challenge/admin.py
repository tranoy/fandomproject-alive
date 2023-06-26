from django.contrib import admin
from .models import *

class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'video_file', 'ref_id')
    
class Ref_VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'singer', 'video_file')
    list_filter = ['title', 'singer']
    
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'score', 'video_file', 'ref_id', 'create_at')
    list_filter = ['nickname', 'score']
    
admin.site.register(Video)
admin.site.register(Ref_Video)
