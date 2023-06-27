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
from accounts.models import User
from django.core.paginator import Paginator
# Create your views here.

# /videogallery 경로 인식 후 index함수가 호출 됨 index함순s html을 렌더링 context포함해서

class ChallengeMain(APIView):
    def get(self,request):
        #Refv = Ref_Video.objects.all()
        max_scores = Score.objects.values('ref_id').annotate(max_scores=Max('score'))
        videos = Ref_Video.objects.filter(id__in = max_scores.values('ref_id')).values('title', 'singer', 'video_file', 'img')
        data_count = Score.objects.values('ref_id').annotate(count=Count('ref_id'))
        data = Score.objects.filter(ref_id__in=videos.values('id'), score=models.Subquery(Score.objects.filter(ref_id=models.OuterRef('ref_id')).values('score').order_by('-score')[:1])).values('nickname', 'score')
        data = data.annotate(id=models.Subquery(videos.filter(id=models.OuterRef('ref_id')).values('id')[:1]),
                             title=models.Subquery(videos.filter(id=models.OuterRef('ref_id')).values('title')[:1]),
                             singer=models.Subquery(videos.filter(id=models.OuterRef('ref_id')).values('singer')[:1]),
                             img=models.Subquery(videos.filter(id=models.OuterRef('ref_id')).values('img')[:1]))

        print(data)
        print(data_count)
        ref_unique_ref_ids = Ref_Video.objects.values_list('id', flat=True)
        score_unique_ref_ids = Score.objects.values_list('ref_id', flat=True).distinct()  # 
        
        try:
            nickname = request.session['nickname']
            user = User.objects.filter(nickname=nickname).first()
        except KeyError:
            nickname = None
            user = None
        # socre에는 없는 ref_id찾기
        missing_ref_ids = set(ref_unique_ref_ids) - set(score_unique_ref_ids)
        print("missing_ref_ids=", missing_ref_ids)
        
        if len(missing_ref_ids) != 0:
            # missing_ref_ids에 대한 데이터 생성
            missing_data = []
            data_count = list(data_count)
            for ref_id in missing_ref_ids:
                missing_data.append({
                    'id': ref_id,
                    'title': Ref_Video.objects.get(id=ref_id).title,
                    'singer': Ref_Video.objects.get(id=ref_id).singer,
                    'img': Ref_Video.objects.get(id=ref_id).img
                })
                data_count.append({'ref_id': ref_id, 'count': 0})

            # 기존 data와 missing_data 병합
            data = list(data) + missing_data
        paginator = Paginator(data_count, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        #####################################################
        combined_data = zip(data, data_count,page_obj)

        context = {'combined_data' : combined_data,
                   'user' : user,
                   'page_obj':page_obj}
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
        ref_video=Ref_Video.objects.get(id=pk)
        context = {'score' : score,
                   'ref' : ref_video,
                   'user' : user}
        return render(request, "challenge/ch1.html", context)
    def post(self, request, pk):
        print("ChallengeOne - POST")
        # if request.method == 'POST':
        #     form = CommentForm(request.POST)
        #     if form.is_valid():
        #         comment = form.save(commit=False)
        #         comment.nickname = request.session['nickname']
        #         comment.ref_id = pk
        #         #comment.content_id = id
        #         comment.save()
        # if request.method == 'POST':
        #     score_id = request.POST.get('score_id')
        #     score = Score.objects.get(id=score_id)
        #     like = Like(nickname=request.session['nickname'], score=score)
        #     like.save()
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
 
# class ChallengeTwo(APIView):
#     def get(self,request):
#         return render(request,"challenge/ch2.html")
    
# class ChallengeThree(APIView):
#     def get(self,request):
#         return render(request,"challenge/ch3.html")

#########################################################    
# class ChallegeUpload1(APIView):
#     def get(self,request):
#         return render(request,"challenge/ch1.html")
#     def post(self, request):
#         form = VideoForm(request.POST, request.FILES)
#         if form.is_valid():
#             video = form.save()
#             return Response({'video': video.id}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
#########################################################
        
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
        # return render(request, "challenge/compare_result.html", {'score': 0})


######################################

def upload_video(request, pk):
    print("upload_video")
    challenge = Ref_Video.objects.get(id=pk)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        form.ref_id = pk
        
        if form.is_valid():
            video = form.save(commit=False)  # commit=False를 사용하여 객체를 임시로 저장
            video.ref_id = pk  # 동영상 객체에 ref_id 할당
            video.save()  # 동영상 객체를 저장
            context = {
                'form': form,
                'challenge': challenge,  # challenge 객체 추가
            }
            return render(request, "challenge/success.html", context)
    else:
        form = VideoForm()
        form.ref_id = pk
        # print('-'*100, form.ref_id, '-'*100)
        
        context = {
            'form': form,
            'challenge': challenge,  # challenge 객체 추가
        }
    return render(request, 'challenge/upload.html', context)

# class upload_video(APIView):
#     def get(self, request):
#         return render(request, )
#     def upload_video(request):
#         if request.method == 'POST' and request.FILES['files']:
#             form = VideoForm(request.POST, request.FILES)
#             if form.is_valid():
#                 video = form.save()  # 동영상 저장
#                 # 모델에 동영상 전달하여 처리
#                 score = compare_video('challenge/static/video/knock_step.mp4', video)
#                 return render(request, "challenge/compare_result.html", {'score': score})
#         else:
#             form = VideoForm()
        
#         return render(request, 'ch1.html', {'form': form})


###################################################
