from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .models import Gallery
from challenge.models import Score, Ref_Video
from django.contrib import messages
from accounts.models import User
from django.db.models import Q
from django.http import JsonResponse
from making.models import TransformedLog
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

# Create your views here.

# /videogallery 경로 인식 후 index함수가 호출 됨 index함순s html을 렌더링 context포함해서
def Main(request):
        query = request.GET.get('query')
        if query:
            scores = Score.objects.filter(Q(nickname__icontains=query)).all()
        else:
            scores = Score.objects.all()
            
        result = []
        try:
            nickname = request.session['nickname']
            user = User.objects.filter(nickname=nickname).first()
        except KeyError:
            nickname = None
            user = None
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
        r_result = result[::-1]
        paginator = Paginator(r_result, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'result' : page_obj,
            'query' : query,
            'user' : user,
        }
        return context
    
def GalleryMain(request):
    context = Main(request)
    
    if request.method == 'POST':
        text = request.POST.get('text')  # 게시글 내용 가져오기
        video_file = request.POST.get('output_path')
        print('-' * 300, text)
        print('='*300, video_file)
        nickname = request.session['nickname']
        score = Score.objects.filter(nickname=nickname).order_by('-id').first()
        ref_video = Ref_Video.objects.get(id=score.ref_id)
        ref_video.title = ref_video.title.replace(' ', '_')
        # video_file = f"output/{nickname}_{ref_video.title}_output.mp4"  # 동영상 파일 업데이트
        # video_file = request.FILES.get('video')  # 업로드된 동영상 파일 가져오기

        score = Score.objects.filter(nickname=nickname, ref_id=score.ref_id).order_by('-id').first()
        score.text = text
        score.video_file = video_file
        score.save()
        
        context = Main(request)
    return render(request, "videogallery/videogallery.html", context)
    

class GalleryMore(APIView):
    def get(self, request, pk):
        scores = Score.objects.filter(id=pk)
        result = []
        try:
            nickname = request.session['nickname']
            user = User.objects.filter(nickname=nickname).first()
        except KeyError:
            messages.warning(request, '로그인 후에 페이지를 사용하실 수 있습니다.')
            return redirect('/login')  # 로그인 페이지로 리디렉션
        for score in scores:
            try:
                ref_video = Ref_Video.objects.get(id=score.ref_id)
                result.append([score.id, score.nickname, score.score, score.text, score.create_at, score.video_file, ref_video.title, ref_video.singer])
                print(result)
            except Ref_Video.DoesNotExist:
                pass
        context = {'result': result,
                   'user':user}
        print(score)
        return render(request, "videogallery/more.html", context)

# def GoUpdate(request, pk):
#     context = {'pk' : pk}
#     return render(request, 'videogallery/videoupdate.html', context)
    
# def Edit(request, pk):

#     if request.method == 'POST':
#         new_text = request.POST.get('new_text')
#         Score.objects.filter(id=pk).update(text=new_text)
#         return redirect('/videogallery/Edit')

def delete(request, pk):
    Score.objects.filter(id=pk).delete()
    
    return redirect('/videogallery')

def Edit(request, pk):
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