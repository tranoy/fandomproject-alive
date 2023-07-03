import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import sigmoid
import sys
import os.path
from PIL import Image
from torchvision import transforms
import numpy as np

class ResidualBlock(nn.Module):
    def __init__(self):
        super(ResidualBlock, self).__init__()
        self.conv_1 = nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1)
        self.conv_2 = nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1)
        self.norm_1 = nn.BatchNorm2d(256)
        self.norm_2 = nn.BatchNorm2d(256)

    def forward(self, x):
        output = F.relu(self.norm_2(self.conv_2(F.relu(self.norm_1(self.conv_1(x))))))
        return output + x

class Transformer_aivle(nn.Module):
    def __init__(self):
        super(Transformer_aivle, self).__init__()
        self.conv_1 = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=7, stride=1, padding=3)
        self.norm_1 = nn.BatchNorm2d(64)
        
        # down-convolution #
        self.conv_2 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=2, padding=1)
        self.conv_3 = nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, stride=1, padding=1)
        self.norm_2 = nn.BatchNorm2d(128)
        
        self.conv_4 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, stride=2, padding=1)
        self.conv_5 = nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1)
        self.norm_3 = nn.BatchNorm2d(256)
        
        # residual blocks #
        residualBlocks = []
        for l in range(8):
            residualBlocks.append(ResidualBlock())
        self.res = nn.Sequential(*residualBlocks)
        
        # up-convolution #
        self.conv_6 = nn.ConvTranspose2d(in_channels=256, out_channels=128, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.conv_7 = nn.ConvTranspose2d(in_channels=128, out_channels=128, kernel_size=3, stride=1, padding=1)
        self.norm_4 = nn.BatchNorm2d(128)

        self.conv_8 = nn.ConvTranspose2d(in_channels=128, out_channels=64, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.conv_9 = nn.ConvTranspose2d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.norm_5 = nn.BatchNorm2d(64)
        
        self.conv_10 = nn.Conv2d(in_channels=64, out_channels=3, kernel_size=7, stride=1, padding=3)

    def forward(self, x):
        x = F.relu(self.norm_1(self.conv_1(x)))
        
        x = F.relu(self.norm_2(self.conv_3(self.conv_2(x))))
        x = F.relu(self.norm_3(self.conv_5(self.conv_4(x))))
        
        x = self.res(x)
        x = F.relu(self.norm_4(self.conv_7(self.conv_6(x))))
        x = F.relu(self.norm_5(self.conv_9(self.conv_8(x))))
        
        x = self.conv_10(x)

        return x


def postprocess(tensor, reduce_color=False, upscale_factor=1.0):
    tensor = tensor.squeeze().cpu().detach().numpy()  # Remove unnecessary dimensions and move tensor to CPU
    tensor = tensor.transpose((1, 2, 0))  # Change from channel first to channel last
    tensor = (tensor + 1) / 2.0  # Normalize from [-1, 1] to [0, 1]
    tensor = tensor.clip(0, 1)  # Clip values to [0, 1]
    
    if reduce_color:
        tensor = np.mean(tensor, axis=2, keepdims=True).repeat(3, axis=2)  # Convert to grayscale and duplicate along color axis

    tensor *= 255  # Scale from [0, 1] to [0, 255]

    if upscale_factor > 1.0:
        tensor = torch.from_numpy(tensor).permute(2, 0, 1).unsqueeze(0)  # Change back to channel first and add batch dimension
        tensor = F.interpolate(tensor, scale_factor=upscale_factor, mode='bilinear')  # Resize
        tensor = tensor.squeeze().permute(1, 2, 0).numpy()  # Remove unnecessary dimensions and change back to channel last

    return tensor.astype("uint8")  # Convert to uint8