from django.db import models
from django.shortcuts import render
from rest_framework.views import APIView
from .forms import VideoForm
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from dance_30 import compare_video
from .models import *
from django.db.models import Max, Count
from .forms import VideoForm
# Create your views here.

# /videogallery 경로 인식 후 index함수가 호출 됨 index함순s html을 렌더링 context포함해서

class ChallengeMain(APIView):
    def get(self,request):
        #Refv = Ref_Video.objects.all()
        max_scores = Score.objects.values('ref_id').annotate(max_scores=Max('score'))
        videos = Ref_Video.objects.filter(id__in = max_scores.values('ref_id')).values('title', 'singer', 'video_file')
        data_count = Score.objects.values('ref_id').annotate(count=Count('ref_id'))
        data = Score.objects.filter(ref_id__in=videos.values('id'), score=models.Subquery(Score.objects.filter(ref_id=models.OuterRef('ref_id')).values('score').order_by('-score')[:1])).values('nickname', 'score')
        data = data.annotate(id=models.Subquery(videos.filter(id=models.OuterRef('ref_id')).values('id')[:1]),
                             title=models.Subquery(videos.filter(id=models.OuterRef('ref_id')).values('title')[:1]),
                             singer=models.Subquery(videos.filter(id=models.OuterRef('ref_id')).values('singer')[:1]))
        combined_data = zip(data, data_count)
        context = {'combined_data' : combined_data}
        return render(request, "challenge/challenge.html", context)
    
class ChallengeOne(APIView):
    """
    get -> page render
    post -> video file 받아오기 유효한지 검사
    """
    def get(self, request, pk):
        print("ChallengeONE - GET")
        score = Score.objects.filter(ref_id=pk)
        ref_video = Ref_Video.objects.get(id=pk)
        context = {'score' : score,
                   'ref' : ref_video}
        return render(request, "challenge/ch1.html", context)
    def post(self, request, pk):
        print("ChallengeOne - POST")
        score = Score.objects.all()
        challenge = Ref_Video.objects.get(id=pk)
        if request.method == 'POST':
            form = VideoForm(request.POST, request.FILES)
            form.ref_id = pk
            # print('='*100, form.ref_id, '='*100)
            if form.is_valid():
                print("form - valid")
                video = form.save(commit=False)
                video.ref_id = pk
                video.save()
                context = { 
                    'form': form,
                    'challenge': challenge,
                    'score': score
                }
                return render(request, "challenge/success.html", context)
            else:
                print("form - invalid")
                # 유효하지 않은 경우에도 form을 context에 포함시켜서 렌더링
                context = {
                    'form': form,
                    'challenge': challenge,
                    'score': score
                }
                return render(request, 'challenge/challenge.html', context)
        else:
            form = VideoForm()
            form.ref_id = pk
            context = {
                'form': form,
                'challenge': challenge,
                'score': score
            }
            
            print("문제없음")
        return render(request, 'challenge/ch1.html', context)


## 추가
class Upload_success(APIView):
    
    def get(self, request, pk):
        print("Upload_success - GET")
        challenge = Ref_Video.objects.get(id=pk)
        context = {
                'challenge': challenge,  # challenge 객체 추가
            }
        return render(request, "challenge/success.html", context)
 
     
        
class ChallengeCompareResult(APIView):
    
    def get(self, request, pk):
        print("ChallengeCompareResult - GET")
        challenge = Ref_Video.objects.get(id=pk)
        
        ref_path = f"./media/{challenge.video_file}"
        
        latest_video_id = Video.objects.all().aggregate(Max('id'))['id__max']
        video = Video.objects.get(id=latest_video_id)
        # print(video.video_file)
        video_path = f"./media/{video.video_file}"
        
        score = compare_video(ref_path, video_path)
        
        nickname = request.session['nickname']
        score_instance = Score(nickname=nickname, score=score, ref_id=pk)
        score_instance.save()
        
        context = {
            'score': score,
            'challenge': challenge
        }
        
        return render(request, "challenge/compare_result.html", context)