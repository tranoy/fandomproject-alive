from django.shortcuts import render
from . models import Gallery
from rest_framework.views import APIView
from .models import Gallery

# Create your views here.

# /videogallery 경로 인식 후 index함수가 호출 됨 index함순s html을 렌더링 context포함해서

class GalleryMain(APIView):
    def get(self,request):
        video_list = Gallery.objects.all() # select * from content_video

        return render(request, "videogallery/videogallery.html",context=dict(videos=video_list))

