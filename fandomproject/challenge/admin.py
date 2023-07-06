from django.contrib import admin
from .models import *

class VideoAdmin(admin.ModelAdmin):
    """
    관리자가 ref_id별로 video_file path를 정의
    Args:
        VideoAdmin(admin.ModelAdmin) = Video 모델에 대한 사용자 정의 관리자 인터페이스를 정의
    """
    # 관리자 목록보기에서 표시할 필드 지정
    list_display = ('id', 'video_file', 'ref_id')

class Ref_VideoAdmin(admin.ModelAdmin):
    """
    관리자가 원본영상(참고영상)을 관리 
    Args:
        Ref_VideoAdmin(admin.ModelAdmin) = Ref_Video 모델에 대한 사용자 정의 관리자 인터페이스를 정의
    """
    # 관리자 목록보기에서 표시할 필드 지정
    list_display = ('id', 'title', 'singer', 'video_file') 
    # 관리자 인터페이스에 'title'과 'singer' 필드에 대한 필터를 추가
    list_filter = ['title', 'singer']  

class ScoreAdmin(admin.ModelAdmin):
    """
    관리자가 사용자가 올린 영상과의 비교 결과를 관리
    Args:
        ScoreAdmin(admin.ModelAdmin) = Score 모델에 대한 사용자 정의 관리자 인터페이스를 정의
    """
    # 관리자 목록보기에서 표시할 필드 지정
    list_display = ('id', 'nickname', 'score', 'video_file', 'ref_id', 'create_at')
    # 관리자 인터페이스에 'nickname'과 'score' 필드에 대한 필터를 추가
    list_filter = ['nickname', 'score']

# 모델을 관리자 인터페이스와 함께 등록
admin.site.register(Video, VideoAdmin)
admin.site.register(Ref_Video, Ref_VideoAdmin)
admin.site.register(Score, ScoreAdmin)
