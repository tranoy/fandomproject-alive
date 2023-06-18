from django.shortcuts import render
from . models import Gallery

# Create your views here.

# /videogallery 경로 인식 후 index함수가 호출 됨 index함순s html을 렌더링 context포함해서
def index(request):
    images = Gallery.objects.all()

    context = {
        'images' : images,
    }
    return render(request, 'videogallery/videogallery.html',context)

def gallery_list(request):
    login_session = request.session.get('')


