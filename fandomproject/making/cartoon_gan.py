from .cartoongan_pytorch_main.network.Transformer import Transformer
import os
import numpy as np
from torchvision import transforms
from torch.autograd import Variable
import torch

class CartoonGAN:
    def __init__(self, model_path, style):
        self.model_path = model_path
        self.style = style
        self.model = Transformer()
        state_dict = torch.load(os.path.join(model_path, style + "_net_G_float.pth"), map_location=torch.device('cuda' if torch.cuda.is_available() else 'cpu'))
        state_dict = {k: v for k, v in state_dict.items() if k in self.model.state_dict()}
        self.model.load_state_dict(state_dict, strict=False)
        self.model.eval()

    def transform_image(self, input_image):
        input_image = input_image.convert("RGB")
        input_image = np.asarray(input_image)
        input_image = input_image[:, :, [2, 1, 0]]
        input_image = transforms.ToTensor()(input_image).unsqueeze(0)
        input_image = -1 + 2 * input_image
        input_image = Variable(input_image).to(self.model.device)
        with torch.no_grad():
            output_image = self.model.forward(input_image)
        output_image = output_image[0]
        output_image = output_image[[2, 1, 0], :, :]
        output_image = output_image.cpu().float() * 0.5 + 0.5
        return output_image

    def save_image(self, output_image, output_path):
        output_image = output_image.detach().cpu()
        transforms.ToPILImage()(output_image).save(output_path)



