from django.shortcuts import render
from rest_framework.views import APIView
from .models import Gallery
from accounts.models import User

# Create your views here.

# /videogallery 경로 인식 후 index함수가 호출 됨 index함순s html을 렌더링 context포함해서

class GalleryMain(APIView):
    def get(self,request):
        video_list = Gallery.objects.all() # select * from content_video
        try:
            # 세션 데이터 가져오기
            nickname = request.session['nickname']
            user = User.objects.filter(nickname=nickname).first()
            print(user)
        except KeyError:
            nickname = None
            user = None

        return render(request, "videogallery/videogallery.html",context=dict(videos=video_list,user=user))
        



