from django.db import models
from django.shortcuts import render
from rest_framework.views import APIView
from .forms import VideoForm
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from dance_30 import compare_video
from .models import *
from django.db.models import Max
from .forms import VideoForm
# Create your views here.

# /videogallery 경로 인식 후 index함수가 호출 됨 index함순s html을 렌더링 context포함해서

class ChallengeMain(APIView):
    def get(self,request):
        #Refv = Ref_Video.objects.all()
        score = Score.objects.all()
        context = {'score' : score}
        return render(request, "challenge/challenge.html", context)
    
class ChallengeOne(APIView):
    """
    get -> page render
    post -> video file 받아오기 유효한지 검사
    """
    def get(self, request, pk):
        print("ChallengeONE - GET")
        challenge = Ref_Video.objects.get(id=pk)
        return render(request, "challenge/ch1.html", {'challenge': challenge})
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
        
        nickname = request.user.nickname
        title = 'sample Title'
        score_instance = Score(user=request.user, nickname=nickname, score=score, title=title)
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
