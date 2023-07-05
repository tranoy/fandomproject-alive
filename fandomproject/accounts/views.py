from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.views.generic import View


class Join(APIView):
    """
    회원가입을 처리하는 APIView
    Args:
        APIView (class):  Django REST Framework의 APIView를 상속받음
    """
    def get(self,request):
        """
        GET 요청을 처리하여 회원가입 페이지를 보여줌
        Args:
            request (HttpRequest): 클라이언트로부터의 GET 요청 객체

        Returns:
            HttpResponse: 회원가입 페이지의 HTML을 포함하는 응답 객체
        """
        return render(request, "accounts/join.html")
    
    def post(self,request):
        """
        POST 요청을 처리하여 회원가입 정보를 받아서 처리

        Args:
            request (HttpRequest): 클라이언트로부터의 POST 요청 객체

        Returns:
            JsonResponse or HttpResponse: 회원가입 결과에 따른 JSON 응답 또는 리다이렉트 응답 객체
        """
        
        # 비동기 요청으로 받은 회원가입 정보
        nickname = request.data.get('nickname',None)
        username = request.data.get('username',None)
        password1 = request.data.get('password1',None)
        password2 = request.data.get('password2',)
        email = request.data.get('email','')
        
        # 닉네임 이메일 중복 확인
        exists = User.objects.filter(email=email).exists()
        nick_exists = User.objects.filter(nickname=nickname).exists()
        
        if nick_exists:
            # 이미 존재하는 닉네임일 경우에 대한 응답
            id_data = {'id_exists':nick_exists}
            return JsonResponse(id_data)

        if exists:
            # 이미 존재하는 이메일일 경우에 대한 응답
            print("post호출")
            data = {'exists':exists}
            return JsonResponse(data)
        
        # 비밀번호 일치여부 확인
        if password1 == password2:
            User.objects.create(nickname=nickname,email=email,username=username,password=make_password(password1))
            # 회원가입 후 로그인 페이지로 리다이렉트
            return redirect('/login')


               
class Login(APIView):
    """
    로그인을 처리하는 APIView
    Args:
        APIView (class)
    """
    def get(self, request):
        """_summary_
        GET 요청을 처리하여 로그인 페이지를 보여줌
        Args:
            request (HttpRequest)

        Returns:
            _type_: HttpResponse
        """
        return render(request, "accounts/login.html")
    def post(self,request):
        """
        POST 요청을 처리하여 로그인 정보 검증 세션 또는 리다이렉트 응답 반환
        Args:
            request (HttpRequest)

        Returns:
            _type_: HttpResponse or Response
        """
        
        # 클라이언트에서 받은 회원 정보
        nickname = request.data.get('nickname',None)
        password = request.data.get('password',None)
        user = User.objects.filter(nickname=nickname).first()
        
        
        if user is None:
            return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))

        if user.check_password(password):
            # 로그인 성공 시 세션에 사용자 닉네임 값 저장
            request.session['nickname'] = nickname
            return redirect('/')
        else:
             return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))



class Checkbox(APIView):
    """
    이용약관을 처리하는 APIView
    Args:
        APIView (class)
    """
    def get(self,request):
        """
        GET 요청시 이용약관 페이지를 보여줌
        Args:
            request (HttpRequest)

        Returns:
            _type_: HttpResponse
        """
        return render(request,'accounts/checkbox.html')
    





class RequestPasswordResetEmail(View):
    """
    계정에 등록된 이메일정보 처리하는 View
    Args:
        View (class)
    """
    def get(self, request):
        """
        GET 요청시 이메일 확인 페이지를 보여줌
        Args:
            request (HttpRequest)

        Returns:
            _type_: HttpResponse
        """
        return render(request, 'accounts/reset-password.html')
    
    def post(self, request):
        """
        POST 요청시 이메일 확인 페이지를 보여줌
        Args:
            request (HttpRequest)

        Returns:
            _type_: HttpResponse
        """
        user_email = request.POST['email']
        
        context = {
            'values':request.POST
        }
        
        # 이메일 유효성 검사
        if not validate_email(user_email):
            messages.error(request, 'Please supply a valid email')
            return render(request, 'accounts/reset-password.html', context)
        
        current_site = get_current_site(request)
        
        user = User.objects.filter(email=user_email)
        
        
        # 이메일 확인
        if user.exists():

            # uid, token으로 비밀번호 재설정 요청의 신뢰선 보안 유효성 검증
            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            }

            link = reverse('reset-user-password', kwargs={
                'uidb64': email_contents['uid'], 'token': email_contents['token']})

            email_subject = 'ALIVE 계정정보 찾기'

            reset_url = 'http://'+current_site.domain + link

            user_email = EmailMessage(
                email_subject,
                'Hi, Please the link below to reset your password \n'+reset_url,
                'noreply@semycolon.com',
                [user_email],
            )
            user_email.send(fail_silently=False)
        
            messages.success(request, 'We have sent you an email to reset your password ')
        
        else:
            messages.error(request, '존재하지 않는 계정입니다.')
        return render(request, 'accounts/reset-password.html')
    
    
class CompletePasswordReset(View):
    """
    비밀번호 재설정를 처리하는 View
    Args:
        View (class):
    """
    def get(self, request, uidb64, token):
        """
        GET 요청을 처리하여 비밀번호 재설정 페이지를 보여줌
        Args:
            request (HttpRequest): _description_
            uidb64 (str): 사용자의 UID를 Base64로 인코딩한 문자열
            token (str): 비밀번호 재설정을 위한 토큰

        Returns:
            _type_: HttpResponse
        """
        
        context={
            'uidb64':uidb64,
            'token':token
        }
        return render(request, 'accounts/set-new-password.html', context)
    
    def post(self, request, uidb64, token):
        """
        POST 요청을 처리하여 비밀번호를 재설정
        Args:
            request (HttpRequest)
            uidb64 (str)
            token (str)

        Returns:
            _type_: HttpResponse
        """
        context={
            'uidb64':uidb64,
            'token':token
        }
        
        password=request.POST['password']
        password2=request.POST['password2']
        
        # 비밀번호 확인
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/set-new-password.html', context)
        
        # 비밀번호 형식 체크
        if len(password) <6:
            messages.error(request, 'Passwords too short')
            return render(request, 'accounts/set-new-password.html', context)
        
        
        try:
            # 사용자 ID 디코딩
            user_id = force_str(urlsafe_base64_decode(uidb64))
            # 사용자 객체 가져오기
            user = User.objects.get(pk=user_id)
            # 비밀번호 설정 및 저장
            user.set_password(password)
            user.save()
            
            messages.success(request, 'Password reset successfull, you can login with your new password')
            return redirect('/login')
        
        except Exception as identifier:

            messages.info(request, 'Something went wrong, try again')
        
            return render(request, 'accounts/set-new-password.html', context)