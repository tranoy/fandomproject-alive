from rest_framework.views import APIView
from django.shortcuts import render,redirect
from accounts.models import User
from making.models import TransformedLog
from django.db.models import Max, Count,Subquery,OuterRef
from challenge.models import *
from django.shortcuts import render



# 메인화면
class Main(APIView):
    """
    메인화면 에 필요한 데이터와 렌더링을 처리하는 View
    Args:
        APIView (class)
    """
    def get(self, request):
        """
        메인화면에 필요한 데이터에 맞게 수정 그리고 화면을 보여줌
        Args:
            request (HttpRequest)

        Returns:
            _type_: HttpResponse
        """
        
        
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
        score_unique_ref_ids = Score.objects.values_list('ref_id', flat=True).distinct()
        
        # score 없는 ref_id찾기
        missing_ref_ids = set(ref_unique_ref_ids) - set(score_unique_ref_ids)
        
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
        try:
            # 세션 데이터 가져오기
            nickname = request.session['nickname']
            user = User.objects.filter(nickname=nickname).first()

        except KeyError:
            nickname = None
            user = None
            
        transformItem = TransformedLog.objects.order_by('-id').all()
        context = {'user': user,
                   'transformItem' : transformItem,
                   'data':data,
                   }
        
        return render(request, 'index.html', context)

# 로그아웃 시 세션 지워야 함
# 로그인 된 상태에서 로그아웃 누를 때
# /logout 경로 요청 시 LogOutClass get 함수 호출 하면서 세션 삭제하고 HOME 경로로 redirection
# 세션 삭제
class LogOut(APIView):
    """
    로그아웃을 처리하는 APIView
    Args:
        APIView (class)
    """
    def get(self, request):
        """
        세션의 데이터를 삭제
        Args:
            request (HttpRequest)
        Returns:
            _type_: Redirect
        """
        request.session.flush()
        return redirect("/")
    
class Privacy(APIView):
    """
    개인정보 처리 방침에 필요한 APIView
    Args:
        APIView (class)
    """
    def get(self,request):
        """
        GET : 개인정보 처리방침 화면을 보여줌
        Args:
            request (HttpRequest):

        Returns:
            _type_: HttpResponse
        """
        return render(request,'privacy.html')
    
class Policy(APIView):
    """
    이용약관을 처리하는 class
    Args:
        APIView (class)
    """
    def get(self,request):
        """
        GET : 이용약관 화면을 보여줌
        Args:
            request (HttpRequest)

        Returns:
            _type_: HttpResponse
        """
        return render(request,'policy.html')