from django.db import models
from django.shortcuts import render
from rest_framework.views import APIView
from challenge.models import Score, Ref_Video
from django.db.models import Count
from accounts.models import User
# Create your views here.



class RankingMain(APIView):
    def get(self,request):
        score_count = Score.objects.count()
        scores = Score.objects.order_by('-score')
        try:
            nickname = request.session['nickname']
            user = User.objects.filter(nickname=nickname).first()
        except KeyError:
            nickname = None
            user = None
        result = []
        for score in scores:
            try:
                ref_video = Ref_Video.objects.get(id=score.ref_id)
                result.append([score.nickname, score.score, ref_video.title, ref_video.singer])
            except Ref_Video.DoesNotExist:
                pass
        context = {'score_count' : score_count,
                   'result' : result,
                   'user' : user,}
        return render(request, 'ranking/ranking.html', context)