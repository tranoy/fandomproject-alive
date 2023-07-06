from django.db import models
from datetime import datetime
from django.conf import settings

# Create your models here.
class Video(models.Model):
    """
    Video 모델 정의
    Args:
        models.Model 클래스를 상속
    """
    video_file = models.FileField(upload_to='challenge_upload/', default=0)    # 업로드된 파일을 저장
    ref_id = models.IntegerField(default=0)                                    # 원본 영상의 id 값을 저장
    
class Ref_Video(models.Model):
    """
    Ref_Video 모델 정의: 원본 영상의 정보를 가지고 있음
    Args:
        models.Model 클래스를 상속
    """
    id = models.AutoField(primary_key=True)                                    # 원본 영상의 id 값을 저장 (==ref_id)
    title = models.CharField(max_length=20)                                    # 영상의 노래 제목
    singer = models.CharField(max_length=10, default=None)                     # 영상의 가수 이름
    video_file = models.FileField(upload_to='ref_video/', default=0)           # 원본 영상의 path (ref_video 폴더 아래에 위치)
    img = models.CharField(max_length=255, default=0)                          # 원본 영상의 앨범 자킷 이미지
    
class Score(models.Model):
    """
    Score 모델 정의: 사용자들이 올린 영상과 원본 영상의 비교 결과를 저장
    Args:
        models.Model 클래스를 상속
    """
    nickname = models.CharField(max_length=255)                                # 사용자의 닉네임
    score = models.FloatField()                                                # 사용자가 올린 영상의 Score
    text = models.TextField(default='-')                                       # 영상을 비교하고 사용자가 작성한 리뷰
    video_file = models.FileField(upload_to='output/', default = 0)            # 사용자의 결과 영상 Path
    ref_id = models.IntegerField(default=0)                                    # 원본 영상의 ID
    create_at = models.DateTimeField(auto_now_add=True)                        # 사용자가 영상을 올린 시간 