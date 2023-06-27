from django.core.files.base import ContentFile
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.files.base import ContentFile
from django.urls import reverse
from .models import TransformedImage
from .cartoongan_pytorch_main.network.Transformer import Transformer
from .cartoongan_pytorch_main.network.Transformer_aivle import Transformer_aivle
import io
import os
import torch
import json
import numpy as np
from PIL import Image
from torchvision import transforms
from torchvision.transforms.functional import to_pil_image
from django.shortcuts import get_object_or_404

model_path = 'making/cartoongan_pytorch_main/pretrained_model/'
styles = ['Hayao', 'Hosoda', 'Shinkai', 'Paprika', 'spongebob', 'simpson', 'anime']

def index(request):
    transform_url = reverse('making:transform')
    context = {'transform_url': transform_url, 'styles': styles}
    return render(request, 'making/making.html', context)

def transform(request):
    if request.method == 'POST':
        if 'image' not in request.FILES:
            return JsonResponse({'error': '이미지 파일이 제공되지 않았습니다.'}, status=400)

        image = request.FILES['image']
        style = request.POST.get('style')

        # 이미지 전처리
        pil_image = Image.open(image)

        # RGB로 변환
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')

        input_image = np.asarray(pil_image)
        input_image = input_image[:, :, [0, 1, 2]]  # RGB에서 BGR로 변경
        input_image = transforms.ToTensor()(input_image).unsqueeze(0)
        input_image = input_image * 2 - 1  # 전처리, (-1, 1)

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # 사전 학습된 모델 불러오기
        if style in ['Hayao', 'Hosoda', 'Shinkai', 'Paprika']:
            model = Transformer()
            state_dict = torch.load(os.path.join(model_path, style + '_net_G_float.pth'), map_location=device)
            model.load_state_dict(state_dict, strict=True)
        elif style in ['spongebob', 'simpson', 'anime']:
            model = Transformer_aivle().to(device)
            state_dict = torch.load(os.path.join(model_path, style + "_net_G_float.pth"), map_location=device)
            model.load_state_dict(state_dict['g_state_dict'])
            model.eval()
        else:
            return JsonResponse({'error': '지원되지 않는 스타일입니다.'}, status=400)

        # 모델을 GPU로 이동
        model = model.to(device)
        input_image = input_image.to(device)

        # 순전파
        with torch.no_grad():
            output_image = model(input_image)
        output_image = output_image[0]
        # BGR에서 RGB로 변경
        output_image = output_image.permute(1, 2, 0).cpu().float()
        output_image = (output_image * 0.5 + 0.5).clamp(0, 1)  # 색상 반전 방지 및 범위 제한

        # 넘파이 배열을 PIL 이미지로 변환
        output_image = Image.fromarray((output_image * 255).byte().cpu().numpy())

        # 이미지를 저장할 임시 파일 생성
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


def display(request):
    transformed_image_id = request.session.get('transformed_image_id')
    if transformed_image_id is not None:
        transformed_image = get_object_or_404(TransformedImage, id=transformed_image_id)
        context = {
            'transformed_image_url': transformed_image.image.url,
            'style': transformed_image.style
        }
        return render(request, 'making/display.html', context)
    else:
        return JsonResponse({'error': '변환된 이미지가 없습니다.'}, status=404)


def download(request):
    transformed_image_id = request.session.get('transformed_image_id')
    if transformed_image_id is not None:
        transformed_image = get_object_or_404(TransformedImage, id=transformed_image_id)
        response = HttpResponse(transformed_image.image, content_type='image/jpeg')
        response['Content-Disposition'] = 'attachment; filename="transformed_image.jpg"'
        return response
    else:
        return HttpResponse('Image not found.', status=404)