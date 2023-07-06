from django.shortcuts import render, redirect
from rest_framework.views import APIView
from challenge.models import Score, Ref_Video
from django.contrib import messages
from accounts.models import User
from django.db.models import Q
from django.http import JsonResponse
from making.models import TransformedLog
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

# Create your views here.
def Main(request):
    """
    html에 전달하기 위한 객체 생성
    Args:
        request (HttpRequest): 클라이언트로부터의 GET 요청 객체 

    Returns:
        html에 전달하는 객체 
    """
    # 검색을 위한 query 설정
    query = request.GET.get('query')
    if query:                                                                                   # query(검색어)가 있을 때
        scores = Score.objects.filter(Q(nickname__icontains=query)).all()                       # Score 모델에서 query와 대응하는 object 추출
    else:                                                                                       # query(검색어)가 없을 때
        scores = Score.objects.all()                                                            # Score 모델에서 전체 object 추출
        
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
            mk_image = TransformedLog.objects.filter(nickname=score.nickname).order_by('-date').first()     # TransformedLog 모델에서 nickname == nickname인 object 중 가장 최근에 만든 object 추출
        except ObjectDoesNotExist:                                                                          # 예외처리: 값이 없을 때 
            mk_image = None
        
        try:
            ref_video = Ref_Video.objects.get(id=score.ref_id)                                              # Ref_Video 모델에서 ref_id == id인 object 추출
        except ObjectDoesNotExist:                                                                          # 예외처리: 값이 없을 때 
            ref_video = None
        # 수집한 데이터 추가 
        # result = [id, nickname, score, text, title, singer, img_url]
        result.append([score.id, score.nickname, score.score, score.text, ref_video.title if ref_video else '', ref_video.singer if ref_video else '', mk_image.image_url if mk_image else '/media/defaultimg.png'])
    
    # 최신 순으로 정렬
    r_result = result[::-1]
    
    # 페이지 전환을 위한 객체
    paginator = Paginator(r_result, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # html에 전달할 객체
    context = {
        'result' : page_obj,
        'query' : query,
        'user' : user,
    }
    return context
    
def GalleryMain(request):
    """
    Videogallery App의 Main URL에 대응하는 함수
    Args:
        request (HttpRequest): 클라이언트로부터의 GET 요청 객체

    Returns:
        HttpRequest: VideoGallery main페이지에서의 응답 객체 
    """
    # videogallery.html에 전달할 객체 생성
    context = Main(request)
    
    # POST 요청을 받았을 때 
    if request.method == 'POST':
        text = request.POST.get('text')                                                                  # 게시글 내용 가져오기
        video_file = request.POST.get('output_path')                                                     # video_path 가지고 오기
        nickname = request.session['nickname']                                                           # 현재 세션에서 nickname 가지고 오기
        # Score, Ref_Video 모델에서 object 추출
        score = Score.objects.filter(nickname=nickname).order_by('-id').first()
        ref_video = Ref_Video.objects.get(id=score.ref_id)
        ref_video.title = ref_video.title.replace(' ', '_')

        # Score 모델의 text, video_file 필드에 새로운 값을 넣고 저장
        score = Score.objects.filter(nickname=nickname, ref_id=score.ref_id).order_by('-id').first()
        score.text = text
        score.video_file = video_file
        score.save()
        
        context = Main(request)
    return render(request, "videogallery/videogallery.html", context)
    

class GalleryMore(APIView):
    """
    게시판에 올라온 글들을 자세히 보기위한 URL에 대응하는 APIView
    Args:
        APIView(class): Django REST Framwork의 APIView를 상속
    """
    def get(self, request, pk):
        """
        GET 요청을 처리
        Args:
            request (HttpRequest): 클라이언트로부터의 GET 요청 객체 
            pk (int): 원본 영상 객체 id
            
        Returns:
            HttpRequest: URL에서의 응답 객체
        """
        # 현재 로그인 상태 확인
        try:
            nickname = request.session['nickname']
            user = User.objects.filter(nickname=nickname).first()
        except KeyError:
            messages.warning(request, '로그인 후에 페이지를 사용하실 수 있습니다.')                 # 경고 메시지
            return redirect('/login')                                                            # 로그인 페이지로 리디렉션
        
        # Score 모델에서 Pk == id인 object 추출
        scores = Score.objects.filter(id=pk)
        # result = 수집한 데이터를 모은 list
        result = []
        for score in scores:
            try:
                # list에 데이터 추가
                # result = [id, nickname, score, text, create_at, video_file, title, singer]
                ref_video = Ref_Video.objects.get(id=score.ref_id)
                result.append([score.id, score.nickname, score.score, score.text, score.create_at, score.video_file, ref_video.title, ref_video.singer])
            except Ref_Video.DoesNotExist:                                                        # 예외 처리: 값이 없을 때 
                pass
        
        # more.html에 전달할 객체
        context = {'result': result,
                   'user':user}
        return render(request, "videogallery/more.html", context)
    
def delete(request, pk):
    """
    게시판에서 삭제할 때 사용하는 함수
    Args:
        request (HttpRequest): 클라이언트로부터의 GET 요청 객체 
        pk (int): 원본 영상 객체 id

    Returns:
        게시판 Main URL로 리디렉션
    """
    # Score 모델에서 id == pk인 object 삭제
    Score.objects.filter(id=pk).delete()
    
    return redirect('/videogallery')

def Edit(request, pk):
    """
    게시판에서 수정할 때 사용하는 함수
    Args:
        request (HttpRequest): 클라이언트로부터의 GET 요청 객체 
        pk (int): 원본 영상 객체 id

    Returns:
        JsonResponse: 해당하는 message를 전달
    """
    # POST 요청을 받을 때
    if request.method == 'POST':
        id = request.POST.get('id')                                         # id와 action을 POST 데이터에서 획득
        action = request.POST.get('action')
        
        if action == 'update':                                              # 수정할 경우(Edit 버튼을 눌렀을 때)
            new_text = request.POST.get('text')                             # text를 POST 데이터에서 획득
            Score.objects.filter(id=id).update(text=new_text)               # Score 모델에서 id에 해당하는 object를 찾아 text필드를 수정
            return JsonResponse({'message': 'Row updated successfully'})    # Json응답 반환 : 성공
    return JsonResponse({'message': 'Invalid request'})                     # Json응답 반환 : POST가 아닐 때 invalid request응답 반환