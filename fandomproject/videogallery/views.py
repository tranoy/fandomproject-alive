from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .models import Gallery
from challenge.models import Score, Ref_Video
from accounts.models import User
from django.db.models import Q
from django.http import JsonResponse
from making.models import TransformedLog
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

# /videogallery 경로 인식 후 index함수가 호출 됨 index함순s html을 렌더링 context포함해서

class GalleryMain(APIView):
    def get(self,request):
        query = request.GET.get('query')
        if query:
            scores = Score.objects.filter(Q(nickname__icontains=query)).all()
        else:
            scores = Score.objects.all()
            
        result = []
        for score in scores:
            try:
                mk_image = TransformedLog.objects.filter(nickname=score.nickname).order_by('-date').first()
            except ObjectDoesNotExist:
                # Handle the case when TransformedLog object does not exist
                mk_image = None
            
            try:
                ref_video = Ref_Video.objects.get(id=score.ref_id)
            except ObjectDoesNotExist:
                # Handle the case when Ref_Video object does not exist
                ref_video = None

            result.append([score.id, score.nickname, score.score, score.text, ref_video.title if ref_video else '', ref_video.singer if ref_video else '', mk_image.image_url if mk_image else '/media/20230424_002724.png'])
            print(score.id)
        context = {
            'result' : result,
            'query' : query
        }
        return render(request, "videogallery/videogallery.html", context)
    def post(self, request):
        if request.method == 'POST':
            id = request.POST.get('id')
            action = request.POST.get('action')
            print(id, action)
            if action == 'update':
                new_text = request.POST.get('text')
                Score.objects.filter(id=id).update(text=new_text)
                return JsonResponse({'message': 'Row updated successfully'})
            elif action == 'delete':
                Score.objects.filter(id=id).delete()
                return JsonResponse({'message': 'Row deleted successfully'})

        return JsonResponse({'message': 'Invalid request'})

class GalleryMore(APIView):
    def get(self, request, pk):
        scores = Score.objects.filter(id=pk)
        result = []
        for score in scores:
            try:
                ref_video = Ref_Video.objects.get(id=score.ref_id)
                result.append([score.id, score.nickname, score.score, score.text, score.create_at, score.video_file, ref_video.title, ref_video.singer])
                print(result)
            except Ref_Video.DoesNotExist:
                pass
        context = {'result': result }
        print(score)
        return render(request, "videogallery/more.html", context)

def GoUpdate(request, pk):
    context = {'pk' : pk}
    return render(request, 'videogallery/videoupdate.html', context)
    
def Edit(request, pk):

    if request.method == 'POST':
        new_text = request.POST.get('new_text')
        Score.objects.filter(id=pk).update(text=new_text)
        return redirect('/videogallery/Edit')

def delete(request, pk):
    Score.objects.filter(id=pk).delete()
    
    return redirect('/videogallery')