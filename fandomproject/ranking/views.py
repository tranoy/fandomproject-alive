from django.db import models
from django.shortcuts import render
from rest_framework.views import APIView
from challenge.models import Score, Ref_Video
from django.db.models import Count, Q
from accounts.models import User
# Create your views here.

class RankingMain(APIView):
    """
    Ranking app의 Main URL에 대응하는 APIView
    Args:
        APIView(class) : Django REST Framework의 APIView를 상속
    """
    def get(self,request):
        """
        GET 요청을 처리, ranking main 페이지와 대응
        Args:
            request (HttpRequest): 클라이언트로부터의 GET 요청 객체

        Returns:
            HttpRequest: ranking main 페이지에서의 응답 객체
        """
        # 검색을 위한 query 설정
        query = request.GET.get('query')
        if query:                                                                                   # query(검색어)가 있을 때
            scores = Score.objects.filter(Q(nickname__icontains=query)).order_by('-score')          # Score 모델에서 score가 높은 순으로 query와 대응하는 object 추출
        else:                                                                                       # query(검색어)가 없을 때
            scores = Score.objects.order_by('-score')                                               # Score 모델에서 score가 높은 순으로 전체 object 추출
            
        score_count = Score.objects.count()                                                         # Score 필드 개수 확인
        
        # User nickname 확인 (로그인 상태 확인)
        try:
            nickname = request.session['nickname']
            user = User.objects.filter(nickname=nickname).first()
        except KeyError:
            nickname = None
            user = None
            
        # result = 수집한 데이터를 모은 list
        result = []
        for score in scores:
            try:
                ref_video = Ref_Video.objects.get(id=score.ref_id)                                  # Ref_Video 모델에서 ref_id == id인 object 추출 
                result.append([score.nickname, score.score, ref_video.title, ref_video.singer])     # result에 추가
            except Ref_Video.DoesNotExist:                                                          # 예외 처리: 데이터가 없을 때 
                pass
        
        # ranking.html에 전달될 객체
        context = {'score_count' : score_count,
                   'result' : result,
                   'user' : user,
                   'query': query}
        return render(request, 'ranking/ranking.html', context)