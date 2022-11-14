from timm.models import create_model
from focalnet import FocalNet
import torch

model = FocalNet()
p1 = torch.load('focalnet_base_lrf_maskrcnn_3x.pth')['state_dict']


new_dict = {k[9:]: v for k, v in p1.items() if k[9:] in km}
model.load_state_dict(new_dict)
