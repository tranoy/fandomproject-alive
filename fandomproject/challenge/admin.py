from django.contrib import admin
from .models import *

class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'video_file', 'ref_id')

class Ref_VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'singer', 'video_file') # 목록에 여러 필드 추가, 밑에 register에도 추가해줘야 함
    list_filter = ['title', 'singer']  # 목록에 검색 필드 추가

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'score', 'video_file', 'ref_id', 'create_at')
    list_filter = ['nickname', 'score']

admin.site.register(Video, VideoAdmin)
admin.site.register(Ref_Video, Ref_VideoAdmin)
admin.site.register(Score, ScoreAdmin)
