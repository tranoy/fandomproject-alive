import torch
import os
import numpy as np
import torchvision.utils as vutils

from PIL import Image
import torchvision.transforms as transforms
from torch.autograd import Variable

from network.Transformer import Transformer
import argparse
import mlflow
import mlflow.pytorch

parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", default="test_img")
parser.add_argument("--load_size", default=256)
parser.add_argument("--model_path", default="./pretrained_model/")
parser.add_argument("--style", default="Shinkai")
parser.add_argument("--output_dir", default="test_output")
parser.add_argument("--gpu", type=int, default=0)

opt = parser.parse_args()

valid_ext = [".jpg", ".png", ".jpeg"]

# Setup MLflow experiment
mlflow.start_run()

# Log parameters
mlflow.log_param("input_dir", opt.input_dir)
mlflow.log_param("model_path", opt.model_path)
mlflow.log_param("style", opt.style)

# load pretrained model
model = Transformer()
state_dict = torch.load(os.path.join(opt.model_path, opt.style + "_net_G_float.pth"), map_location=torch.device('cuda' if torch.cuda.is_available() else 'cpu'))
state_dict = {k: v for k, v in state_dict.items() if k in model.state_dict()}
model.load_state_dict(state_dict, strict=False)
model.eval()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

for files in os.listdir(opt.input_dir):
    ext = os.path.splitext(files)[1]
    if ext not in valid_ext:
        continue
    # load image
    input_image = Image.open(os.path.join(opt.input_dir, files)).convert("RGB")
    input_image = np.asarray(input_image)
    # RGB -> BGR
    input_image = input_image[:, :, [2, 1, 0]]
    input_image = transforms.ToTensor()(input_image).unsqueeze(0)
    # preprocess, (-1, 1)
    input_image = -1 + 2 * input_image
    input_image = Variable(input_image).to(device)

    # forward
    with torch.no_grad():
        output_image = model(input_image)
    output_image = output_image[0]
    # BGR -> RGB
    output_image = output_image[[2, 1, 0], :, :]
    output_image = output_image.cpu().float() * 0.5 + 0.5
    # save
    vutils.save_image(
        output_image,
        os.path.join(opt.output_dir, files[:-4] + "_" + opt.style + ".jpg"),
    )
    # Log output image as artifact
    mlflow.log_artifact(os.path.join(opt.output_dir, files[:-4] + "_" + opt.style + ".jpg"))

# End MLflow run
mlflow.end_run()

print("Done!")