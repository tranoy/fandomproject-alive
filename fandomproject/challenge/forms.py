from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    """
    Django form을 정의
    Args:
        forms.ModelForm 클래스 상속
    """
    class Meta:
        model = Video # VideoForm이 Video 모델과 연결
        fields = ('video_file',) # form에서 사용할 필드 지정