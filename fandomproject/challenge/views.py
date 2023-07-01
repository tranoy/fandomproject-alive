from django.db import models
from django.shortcuts import render
from rest_framework.views import APIView
from .forms import VideoForm
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from dance_30 import compare_video
from .models import *
from django.db.models import Max, Count,Subquery,OuterRef
from .forms import VideoForm
from accounts.models import User
from django.core.paginator import Paginator
# Create your views here.

# /videogallery 경로 인식 후 index함수가 호출 됨 index함순s html을 렌더링 context포함해서

def get_ref_video_count():
    return Ref_Video.objects.count()


class ChallengeMain(APIView):
    def get(self,request):
        #Refv = Ref_Video.objects.all()
        max_scores = Score.objects.values('ref_id').annotate(max_scores=Max('score'))
        videos = Ref_Video.objects.filter(id__in = max_scores.values('ref_id')).values('title', 'singer', 'video_file', 'img')
        data_count = Score.objects.values('ref_id').annotate(count=Count('ref_id'))
        
        subquery = Score.objects.filter(ref_id=OuterRef('ref_id')).order_by('-score', 'id')
        data = Score.objects.filter(
            ref_id__in=videos.values('id'), 
            score=Subquery(subquery.values('score')[:1]),
            id=Subquery(subquery.values('id')[:1])).values('nickname','score')
        data = data.annotate(id=Subquery(videos.filter(id=OuterRef('ref_id')).values('id')[:1]),
                             title=Subquery(videos.filter(id=OuterRef('ref_id')).values('title')[:1]),
                             singer=Subquery(videos.filter(id=OuterRef('ref_id')).values('singer')[:1]),
                             img=Subquery(videos.filter(id=OuterRef('ref_id')).values('img')[:1])).order_by('id')


        ref_unique_ref_ids = Ref_Video.objects.values_list('id', flat=True)
        score_unique_ref_ids = Score.objects.values_list('ref_id', flat=True).distinct()  # 
        # socre에는 없는 ref_id찾기
        missing_ref_ids = set(ref_unique_ref_ids) - set(score_unique_ref_ids)
        try:
            nickname = request.session['nickname']
            user = User.objects.filter(nickname=nickname).first()
        except KeyError:
            nickname = None
            user = None
        
        print("missing_ref_ids=", missing_ref_ids)
        
        if missing_ref_ids != 0:
            # missing_ref_ids에 대한 데이터 생성
            missing_data = []
            data_count = list(data_count)
            for ref_id in missing_ref_ids:
                ref = Ref_Video.objects.get(id=ref_id)
                missing_data.append({
                    'id': ref_id,
                    'title': ref.title,
                    'singer': ref.singer,
                    'img': ref.img
                })
                data_count.append({'ref_id': ref_id, 'count': 0})

            # 기존 data와 missing_data 병합
            data = list(data) + missing_data
            
        paginator = Paginator(data, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        #####################################################
        # 다음 페이지로 넘어갈 때 첫 번째 게시물 설정
        print(page_obj)
        print(data_count)

        context = {'page_obj':page_obj,
                   'user' : user,
                   }
        
                   #'score_count' : data_count}
        return render(request, "challenge/challenge.html", context)
    
class ChallengeOne(APIView):
    """
    get -> page render
    post -> video file 받아오기 유효한지 검사
    """
    def get(self, request, pk):
        
        print("ChallengeONE - GET")
        try:
            nickname = request.session['nickname']
            user = User.objects.filter(nickname=nickname).first()
        except KeyError:
            nickname = None
            user = None
            
        
        score = Score.objects.filter(ref_id=pk)
        print(score)
        ref_video=Ref_Video.objects.get(id=pk)
        
        score = list(reversed(score))
        paginator = Paginator(score, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'score' : page_obj,
                   'ref' : ref_video,
                   'user' : user}
        return render(request, "challenge/ch1.html", context)
    
    def post(self, request, pk):
        try:
            nickname = request.session['nickname']
            user = User.objects.filter(nickname=nickname).first()
        except KeyError:
            nickname = None
            user = None
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
                    'score': score,
                    'user' : user
                }
                return render(request, "challenge/success.html", context)
            else:
                print("form - invalid")
                ChallengeOne.get(self,request,pk)
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

    

class ChallengeCompareResult(APIView):
    
    def get(self, request, pk):
        print("ChallengeCompareResult - GET")
        challenge = Ref_Video.objects.get(id=pk)
        
        ref_path = f"./media/{challenge.video_file}"
        
        latest_video_id = Video.objects.all().aggregate(Max('id'))['id__max']
        video = Video.objects.get(id=latest_video_id)
        video_path = f"./media/{video.video_file}"
        
        
        
        nickname = request.session['nickname']
        challenge.title = challenge.title.replace(' ', '_')
        score, output_path = compare_video(ref_path, video_path,nickname,challenge.title)
        print(output_path)
        score_instance = Score(nickname=nickname, score=score, ref_id=pk)
        score_instance.save()
        
        res = Score.objects.filter(nickname=nickname, ref_id=pk).order_by('-id').first()
        
        context = {
            'score': score,
            'challenge': challenge,
            'output_path' : output_path[1:],
            'res' : res
        }
        
        return render(request, "challenge/compare_result.html", context)
    

