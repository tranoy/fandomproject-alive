from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.base import ContentFile
from django.urls import reverse
from PIL import Image
from torchvision import transforms
import numpy as np
import torch
import os
import io
import json
from .models import TransformedImage, TransformedLog
from .cartoongan_pytorch_main.network.Transformer import Transformer
from django.contrib.auth.decorators import login_required

from .cartoongan_pytorch_main.network.Transformer_aivle import Transformer_aivle,postprocess
from django.contrib import messages
from accounts.models import User
from django.utils import timezone



model_path = 'making/cartoongan_pytorch_main/pretrained_model/'
styles = ['Hayao', 'Hosoda', 'Shinkai', 'Paprika', 'spongebob', 'simpson', 'anime']

def index(request):
    transform_url = reverse('making:transform')
    try:
        nickname = request.session['nickname']
        user = User.objects.filter(nickname=nickname).first()
    except KeyError:
        messages.warning(request, '로그인 후에 페이지를 사용하실 수 있습니다.')
        return redirect('/login')  # 로그인 페이지로 리디렉션
    context = {'transform_url': transform_url,
               'styles': styles,
               'user': user}
    return render(request, 'making/making.html', context)


# 사용자로부터 이미지와 스타일을 입력 받고, 해당 스타일로 이미지를 변환
def transform(request):
    if request.method == 'POST':
        if 'image' not in request.FILES:
            return JsonResponse({'error': '이미지 파일이 제공되지 않았습니다.'}, status=400)

        image = request.FILES['image']
        style = request.POST.get('style')

        # PIL 라이브러리를 사용하여 이미지를 RGB로 변환하고, 텐서로 변환
        pil_image = Image.open(image)
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')


        # 또한 픽셀 값을 [-1, 1]로 정규화
        input_image = np.asarray(pil_image)
        input_image = transforms.ToTensor()(input_image).unsqueeze(0)
        input_image = input_image * 2 - 1  # 전처리, (-1, 1)

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # 스타일에 따라 서로 다른 사전 학습된 모델을 불러옴
        if style in ['Hayao', 'Hosoda', 'Shinkai', 'Paprika']:
            model = Transformer()
            state_dict = torch.load(os.path.join(model_path, style + '_net_G_float.pth'), map_location=device)
            model.load_state_dict(state_dict, strict=True)
        elif style in ['spongebob', 'simpson', 'anime']:
            model = Transformer_aivle().to(device)
            state_dict = torch.load(os.path.join(model_path, style + "_net_G_float.pth"), map_location=device)
            model.load_state_dict(state_dict['g_state_dict'])
        else:
            return JsonResponse({'error': '지원되지 않는 스타일입니다.'}, status=400)

        # 모델을 이용해 이미지를 변환
        model = model.to(device)
        input_image = input_image.to(device)
        
        with torch.no_grad():
            output_image = model(input_image)

        # 후처리
        if style in ['spongebob', 'simpson', 'anime']:
            output_image = postprocess(output_image, reduce_color=False)
        else:
            output_image = postprocess(output_image, reduce_color=False)

        output_image = Image.fromarray(output_image.astype(np.uint8))


        # 변환된 이미지를 후처리하여 PIL 이미지로 바꾸고 JPEG 형식의 바이트로 저장
        temp_image_buffer = io.BytesIO()
        output_image.save(temp_image_buffer, format='JPEG')

        # 변환된 이미지를 데이터베이스에 저장
        transformed_image = TransformedImage(style=style)
        transformed_image.image.save('transformed_image.jpg', ContentFile(temp_image_buffer.getvalue()))

        # 세션에 변환된 이미지 정보 저장
        request.session['transformed_image_id'] = transformed_image.id

        # 성공 응답 생성
        response_data = {
            'success': True,
            'transformed_image_url': transformed_image.image.url
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return JsonResponse({'error': '잘못된 요청 메서드입니다.'}, status=405)


# 세션에서 변환된 이미지 ID를 가져와서 이미지를 표시
def display(request):
    transformed_image_id = request.session.get('transformed_image_id')

    if transformed_image_id is None:
        return JsonResponse({'error': '변환된 이미지가 없습니다.'}, status=404)


    transformed_image = get_object_or_404(TransformedImage, id=transformed_image_id)
    transformitem = TransformedImage.objects.all()
    transformed_logs = TransformedLog.objects.all()  # TransformedLog 데이터 가져오기

    # 변환된 이미지 정보를 세션에 저장
    try:
        nickname = request.session['nickname']
        user = User.objects.filter(nickname=nickname).first()
        transformed_image.nickname = nickname
        transformed_image.save()
    except KeyError:
        messages.warning(request, '로그인 후에 페이지를 사용하실 수 있습니다.')
        return redirect('/login')  # 로그인 페이지로 리디렉션

    # 사용자의 닉네임을 가져와서 변환된 이미지와 연결
    post_image_url = reverse('making:post_image')

    context = {
        'transformitem': transformitem,
        'transformed_image_url': transformed_image.image.url,
        'nickname': nickname,
        'user': user,
        'post_image_url': post_image_url,
        'transformed_logs': transformed_logs,  # TransformedLog 데이터를 context에 추가
    }

    return render(request, 'making/display.html', context)

# 사용자의 닉네임과 이미지 URL을 받아서 데이터베이스에 저장
def post_image(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nickname = data.get('nickname')
        image_url = data.get('image_url')
        print(nickname, image_url)
        # TransformedLog 모델에 데이터 저장 로직 작성
        transformed_log = TransformedLog(nickname=nickname, image_url=image_url, date=timezone.now())
        transformed_log.save()

        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

# 세션에서 변환된 이미지 ID를 가져와서 이미지를 다운로드합니다.
def download(request):
    transformed_image_id = request.session.get('transformed_image_id')
    if transformed_image_id is not None:
        transformed_image = get_object_or_404(TransformedImage, id=transformed_image_id)
        response = HttpResponse(transformed_image.image, content_type='image/jpeg')
        response['Content-Disposition'] = 'attachment; filename="transformed_image.jpg"'
        return response
    else:
        return HttpResponse('Image not found.', status=404)