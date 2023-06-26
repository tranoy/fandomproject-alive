import io
import torch

from django.shortcuts import render
from django.http import JsonResponse
from PIL import Image
import numpy as np
from torchvision import transforms
import base64
from django.urls import reverse
from rest_framework.views import APIView
from accounts.models import User
from .cartoongan_pytorch_main.network.Transformer import Transformer



class CartoonGAN:
    def __init__(self, model_path, style):
        self.model_path = model_path
        self.style = style
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = Transformer().to(self.device)
        self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
        self.model.eval()

    def transform_image(self, image):
        with torch.no_grad():
            image = image.to(self.device)
            transformed_image = self.model(image)
        return transformed_image



model_path = 'making/cartoongan_pytorch_main/pretrained_model/Hosoda_net_G_float.pth'
styles = ['Hosoda', 'Shinkai', 'Paprika', 'spongebob']


# MakPage tranform_url, User session 가져오기 , making.html 렌더
class Index(APIView):
    def get(self, request):
        transform_url = reverse('making:transform')
        data = {'transform_url': transform_url, 'styles': styles}
        try:
            # 세션 데이터 가져오기
            nickname = request.session['nickname']
            user = User.objects.filter(nickname=nickname).first()
            print(user)
        except KeyError:
            nickname = None
            user = None
        return render(request, 'making/making.html',context=dict(user=user,data=data))



def transform(request):
    if request.method == 'POST':
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image file provided.'}, status=400)

        image = request.FILES['image']
        style = request.POST.get('style', 'Hosoda')

        # Preprocess image
        pil_image = Image.open(image)

        # Convert to RGB if necessary
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')

        input_image = np.asarray(pil_image)
        input_image = input_image[:, :, [2, 1, 0]]  # RGB to BGR
        input_image = transforms.ToTensor()(input_image).unsqueeze(0)
        input_image = -1 + 2 * input_image  # preprocess, (-1, 1)

        # Load pretrained model
        model = CartoonGAN(model_path, style)
        input_image = torch.FloatTensor(input_image).to(model.device)

        output_image = model.transform_image(input_image)

        # Convert tensor to numpy array
        output_image = output_image[0].cpu().detach().numpy()
        output_image = output_image.transpose((1, 2, 0))
        output_image = (output_image + 1) / 2  # scale from (-1, 1) to (0, 1)
        output_image = (output_image * 255).astype(np.uint8)

        # Reverse BGR to RGB
        output_image = output_image[:, :, [2, 1, 0]]

        # Convert numpy array to PIL image
        output_image = Image.fromarray(output_image)

        # Encode output image as Base64
        buffered = io.BytesIO()
        output_image.save(buffered, format='JPEG')
        encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

        request.session['transformed_image'] = encoded_image
        return JsonResponse({'success': True})

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

def display(request):
    transformed_image = request.session.get('transformed_image', None)
    return render(request, 'making/display.html', {'transformed_image': transformed_image})
