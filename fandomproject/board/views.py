from django.shortcuts import render,get_object_or_404
# Create your views here.


def index(request):
    return render(request, 'board/board.html')

def viewVideo(request,pk):
    return render(request, 'board/video.html')

def addVideo(request):
    return render(request, 'board/add.html')



