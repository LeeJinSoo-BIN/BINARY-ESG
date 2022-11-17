from timm.models import create_model
from focalnet import FocalNet
import torch

model = FocalNet()
p1 = torch.load('focalnet_base_lrf_maskrcnn_3x.pth')['state_dict']


new_dict = {k[9:]: v for k, v in p1.items() if k[9:] in km}
model.load_state_dict(new_dict)

#python -m torch.distributed.launch --nproc_per_node 1 --master_port 12345 tools/test.py configs/focalnet/mask_rcnn_focalnet_base_patch4_mstrain_480-800_adamw_3x_coco_lrf.py focalnet_base_lrf_maskrcnn_3x.pth --cfg-options data.samples_per_gpu=1 model.backbone.focal_levels='[3,3,3,3]'