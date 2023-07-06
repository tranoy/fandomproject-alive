from django.db import models
from django.shortcuts import render,redirect
from rest_framework.views import APIView
from .forms import VideoForm
from django.contrib import messages
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

class ChallengeMain(APIView):
    """
    Challenge app의 Main Url에 대응하는 APIView
    Args:
        APIView(class): Django REST Framework의 APIView를 상속
    """
    def get(self,request):
        """
        GET 요청을 처리, challenge main페이지와 대응
        Args:
            request (HttpRequest): 클라이언트로부터의 GET 요청 객체 

        Returns:
            HttpRequest: challenge main페이지에서의 응답 객체 
        """
        # Score 테이블에서 ref_id 별 사용자 수
        data_count = Score.objects.values('ref_id').annotate(count=Count('ref_id'))
        # Score 테이블에서 ref_id 별로 가장 높은 score를 가진 object
        max_scores = Score.objects.values('ref_id').annotate(max_scores=Max('score'))
        # Ref_Video 테이블에서 max_scores에 대응하는 object 추출
         # -> data = [score, id, ref_id, title, singer, img]
        videos = Ref_Video.objects.filter(id__in = max_scores.values('ref_id')).values('title', 'singer', 'video_file', 'img')
        subquery = Score.objects.filter(ref_id=OuterRef('ref_id')).order_by('-score', 'id')
        data = Score.objects.filter(
            ref_id__in=videos.values('id'), 
            score=Subquery(subquery.values('score')[:1]),
            id=Subquery(subquery.values('id')[:1])).values('nickname','score')
        data = data.annotate(id=Subquery(videos.filter(id=OuterRef('ref_id')).values('id')[:1]),
                             title=Subquery(videos.filter(id=OuterRef('ref_id')).values('title')[:1]),
                             singer=Subquery(videos.filter(id=OuterRef('ref_id')).values('singer')[:1]),
                             img=Subquery(videos.filter(id=OuterRef('ref_id')).values('img')[:1])).order_by('id')

        # 같은 score를 가진 object일 때 중복 처리 (하나만 가지고 오도록)
        ref_unique_ref_ids = Ref_Video.objects.values_list('id', flat=True)
        score_unique_ref_ids = Score.objects.values_list('ref_id', flat=True).distinct()  # 
        # Score 테이블에서 ref_id에 대응하는 score object가 없을 때 
        missing_ref_ids = set(ref_unique_ref_ids) - set(score_unique_ref_ids)
        try:
            nickname = request.session['nickname']
            user = User.objects.filter(nickname=nickname).first()
        except KeyError:  # 예외처리: 값이 없을때
            nickname = None
            user = None
        # score object가 없을 때 
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
        # 위에서 수집한 데이터 처리
        result = []                                 # 위에서 수집한 데이터를 전부 모은 list
        d_count = 0                                 # Ref_id
        for d in data:
            try:
                data_nickname = d['nickname']       # 최고득점자 nickname
            except KeyError:                        # 예외 처리: 값이 없을 때
                data_nickname = None
            try:
                data_score = d['score']             # 최고득점자 score
            except KeyError:                        # 예외 처리: 값이 없을 때 
                data_score = None
            try:
                data_id = d['id']                   # 최고득점자 score id
            except KeyError:                        # 예외 처리: 값이 없을 때
                data_id = None
            try:
                data_title = d['title']             # ref_id에 대응하는 곡 제목
            except KeyError:                        # 예외 처리: 값이 없을 때
                data_title = None
            try:
                data_singer = d['singer']           # ref_id에 대응하는 가수
            except KeyError:                        # 예외 처리: 값이 없을 때
                data_singer = None
            try:
                data_img = d['img']                 # ref_id에 대응하는 노래 앨범 자킷
            except KeyError:                        # 예외 처리: 값이 없을 때
                data_img = None
            result.append([data_nickname, data_score, data_id, data_title, data_singer, data_img, data_count[d_count]['count']])
            d_count += 1
        #print(result)
        # 화면에 보이는 게시물이 6개가 넘어갈때 page전환을 위한 객체
        paginator = Paginator(result, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # challenge.html에 전달할 객체
        context = {'page_obj':page_obj,
                   'user' : user}
        return render(request, "challenge/challenge.html", context)
    
class ChallengeOne(APIView):
    """
    Challenge 객체를 구성하는 URL에 대응하는 APIView
    Args:
        APIView(class): Django REST Framwork의 APIView를 상속
    """
    def get(self, request, pk):
        """
        GET 요청을 처리, challenge/<pk> URL과 대응
        Args:
            request (HttpRequest): 클라이언트로부터의 GET 요청 객체 
            pk (int): challenge를 구성하는 객체 id

        Returns:
             HttpRequest: challenge/<pk> URL에서의 응답 객체 
        """
        print("ChallengeONE - GET")
        # 현재 로그인 상태 확인
        try:
            nickname = request.session['nickname']
            user = User.objects.filter(nickname=nickname).first()
        except KeyError:
            messages.warning(request, '로그인 후에 페이지를 사용하실 수 있습니다.')        # 경고 메시지
            return redirect('/login')                                                   # 로그인 페이지로 리디렉션
            
        # Score, Ref_Video 테이블에서 pk == ref_id(id) 인 object 추출
        score = Score.objects.filter(ref_id=pk)
        ref_video=Ref_Video.objects.get(id=pk)
        # 최신순으로 정렬
        score = list(reversed(score))
        
        # page 전환을 위한 객체
        paginator = Paginator(score, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # ch1.html에 전달할 객체
        context = {'score' : page_obj,
                   'ref' : ref_video,
                   'user' : user}
        return render(request, "challenge/ch1.html", context)
    
    def post(self, request, pk):
        """
        POST 요청을 처리하여 사용자 Upload 처리
        Args:
            request (HttpRequest): 클라이언트로부터의 POST 요청 객체 
            pk (int): challenge를 구성하는 객체 id

        Returns:
            HttpRequest: challenge/<pk> URL or challenge/success.html에서의 응답 객체 
        """
        print("ChallengeOne - POST")
        # 현재 로그인 상태 확인
        try:
            nickname = request.session['nickname']
            user = User.objects.filter(nickname=nickname).first()
        except KeyError:
            messages.warning(request, '로그인 후에 페이지를 사용하실 수 있습니다.')        # 경고 메시지
            return redirect('/login')                                                   # 로그인 페이지로 리디렉션
        
        # Score, Ref_Video 모델에서 object 추출
        score = Score.objects.all()
        challenge = Ref_Video.objects.get(id=pk)
        
        # POST 요청을 받았을 때 
        if request.method == 'POST':
            form = VideoForm(request.POST, request.FILES)                               # POST 데이터와 파일 데이터를 전달하여 초기화
            form.ref_id = pk
            if form.is_valid():                                                         # form 유효성 검사 => 유효한 경우
                print("form - valid")
                video = form.save(commit=False)                                         # video 객체를 생성
                video.ref_id = pk
                video.save()
                context = {                                                             # success.html에 전달할 객체
                    'form': form,
                    'challenge': challenge,
                    'score': score,
                    'user' : user
                }
                return render(request, "challenge/success.html", context)
            else:                                                                       # form 유효성 검사 => 유효하지 않은 경우
                print("form - invalid")
                ChallengeOne.get(self,request,pk)
        else:                                                                           # POST 메서드가 아닐 때
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
    """
    Challenge score result를 구성하는 URL에 대응하는 APIView
    Args:
        APIView(class): Django REST Framwork의 APIView를 상속
    """
    def get(self, request, pk):
        """
        GET 요청을 처리
        Args:
            request (HttpRequest): 클라이언트로부터의 GET 요청 객체 
            pk (int): challenge를 구성하는 객체 id

        Returns:
            HttpRequest: result URL에서의 응답 객체 
        """
        print("ChallengeCompareResult - GET")
        # 현재 로그인 상태 확인
        try:
            nickname = request.session['nickname']
            user = User.objects.filter(nickname=nickname).first()
        except KeyError:
            messages.warning(request, '로그인 후에 페이지를 사용하실 수 있습니다.')                # 경고 메시지
            return redirect('/login')                                                           # 로그인 페이지로 리디렉션
        
        # 원본영상 Object 추출
        challenge = Ref_Video.objects.get(id=pk)                                                # Ref_Video 모델에서 원본영상 object 추출
        ref_path = f"./media/{challenge.video_file}"                                            # 원본 영상 path 설정
        
        # 사용자 영상 Object 추출
        latest_video_id = Video.objects.all().aggregate(Max('id'))['id__max']                   # Video 모델에서 사용자 object 추출
        video = Video.objects.get(id=latest_video_id)
        video_path = f"./media/{video.video_file}"                                              # 사용자 영상 path 설정
        
        # title 전처리
        challenge.title = challenge.title.replace(' ', '_')
        
        # 자세 비교 AI 모델 사용
        score, output_path = compare_video(ref_path, video_path, nickname, challenge.title)
        print(output_path)
        score_instance = Score(nickname=nickname, score=score, ref_id=pk)                       # 모델 결과를 Score 테이블에 저장
        score_instance.save()                                                                   #
        
        res = Score.objects.filter(nickname=nickname, ref_id=pk).order_by('-id').first()
        
        # compare_result.html로 전달하는 객체
        context = {
            'score': score,
            'challenge': challenge,
            'output_path' : output_path[1:],
            'res' : res,
            'user': user
        }
        return render(request, "challenge/compare_result.html", context)
    

