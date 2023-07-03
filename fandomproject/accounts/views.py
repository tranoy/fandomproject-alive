from django.shortcuts import render,redirect
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from django.http import JsonResponse
import json
# from django.contrib.auth.models import User

# 비밀번호 찾기 라이브러리
# 이메일 인증에 필요한 모듈 pip install validate_email
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import PasswordResetTokenGenerator
from .utils import account_activation_token
from django.urls import reverse
from django.contrib import auth

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.views.generic import View
# Create your views here.


class Join(APIView):
    def get(self,request):
        return render(request, "accounts/join.html")
    
    def post(self,request):
        nickname = request.data.get('nickname',None)
        username = request.data.get('username',None)
        password1 = request.data.get('password1',None)
        password2 = request.data.get('password2',)
        email = request.data.get('email','')
        print("post")
        exists = User.objects.filter(email=email).exists()
        nick_exists = User.objects.filter(nickname=nickname).exists()
        print("nickname",nick_exists)
        if nick_exists:
            id_data = {'id_exists':nick_exists}
            return JsonResponse(id_data)
        print("email",exists)
        if exists:
            print("post호출")
            data = {'exists':exists}
            return JsonResponse(data)
        
        # 비밀번호 일치하는지 확인
        if password1 == password2:
            User.objects.create(nickname=nickname,email=email,username=username,password=make_password(password1))
            # 로그인 정보 session에 저
            return redirect('/login')
        
        
        # 닉네임 중복여부 확인 

               
class Login(APIView):
    def get(self, request):
        return render(request, "accounts/login.html")
    def post(self,request):
        nickname = request.data.get('nickname',None)
        password = request.data.get('password',None)
        user = User.objects.filter(nickname=nickname).first()
        if user is None:
            return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))

        if user.check_password(password):
            # 로그인을 했다. 세션 or 쿠키에 삽입
            request.session['nickname'] = nickname
            return redirect('/')
        else:
             return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))

class Checkbox(APIView):
    def get(self,request):
        return render(request,'accounts/checkbox.html')
    


######################### 비밀번호 찾기 추가 부분

from django.contrib.auth import get_user_model

User = get_user_model()

class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'accounts/reset-password.html')
    
    def post(self, request):
        user_email = request.POST['email']
        
        context = {
            'values':request.POST
        }
        
        if not validate_email(user_email):
            messages.error(request, 'Please supply a valid email')
            return render(request, 'accounts/reset-password.html', context)
        
        current_site = get_current_site(request)
        
        user = User.objects.filter(email=user_email)
        
        if user.exists():
            #추가 코드
            # user_instance = user.first()
            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            }
            # 장고 기본 : password_reset_confirm
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
        
        
            # email_body = render_to_string('accounts/reset-password-email.html', {
            #     'reset_url': reset_url
            # })
            
            # email = EmailMessage(email_subject, email_body, to=[user_email])
        
            messages.success(request, 'We have sent you an email to reset your password ')
        
        else:
            messages.error(request, '존재하지 않는 계정입니다.')
        return render(request, 'accounts/reset-password.html')
    
    
class CompletePasswordReset(View):
    # template_name='accounts/set-new-password.html'
    # success_url='/accounts/set-new-password'
    def get(self, request, uidb64, token):
        
        context={
            'uidb64':uidb64,
            'token':token
        }
        return render(request, 'accounts/set-new-password.html', context)
    
    def post(self, request, uidb64, token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['password']
        password2=request.POST['password2']
        
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/set-new-password.html', context)
        
        if len(password) <6:
            messages.error(request, 'Passwords too short')
            return render(request, 'accounts/set-new-password.html', context)
        
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            # 기존 : user.password = password
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            
            messages.success(request, 'Password reset successfull, you can login with your new password')
            return redirect('/login')
        
        except Exception as identifier:

            messages.info(request, 'Something went wrong, try again')
        
            return render(request, 'accounts/set-new-password.html', context)