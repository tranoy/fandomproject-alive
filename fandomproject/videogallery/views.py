from django.shortcuts import render
from rest_framework.views import APIView
from .models import Gallery
from challenge.models import Score, Ref_Video
from accounts.models import User
from django.db.models import Q
from django.http import JsonResponse


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
        print(scores)
        for score in scores:
            try:
                # 세션 데이터 가져오기
                # nickname = request.session['nickname']
                # user = User.objects.filter(nickname=nickname).first()
                # #print(user)
                
                ref_video = Ref_Video.objects.get(id=score.ref_id)
                result.append([score.id, score.nickname, score.score, score.text, ref_video.title, ref_video.singer])
                print(score.id)
            except Ref_Video.DoesNotExist:
                pass
        
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



