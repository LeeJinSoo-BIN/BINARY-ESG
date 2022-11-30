#!pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html

# install mmcv-full thus we could use CUDA operators
#!pip install mmcv-full -f https://download.openmmlab.com/mmcv/dist/cu111/torch1.9.0/index.html

# Copyright (c) OpenMMLab. All rights reserved.
#!pip install terminaltables
import argparse
import copy
import os
import os.path as osp
import time
import warnings

import mmcv
import torch
import torch.distributed as dist
from mmcv import Config, DictAction
from mmcv.runner import get_dist_info, init_dist
from mmcv.utils import get_git_hash

from mmdet import __version__
from mmdet.apis import init_random_seed, set_random_seed, train_detector
from mmdet.datasets import build_dataset
from mmdet.models import build_detector
from mmdet.utils import (collect_env, get_device, get_root_logger,
                         replace_cfg_vals, setup_multi_processes,
                         update_data_root)
from mmdet.apis import init_detector, inference_detector
import pdb;



from mmcv.runner import load_checkpoint

CONFIG_FILE = 'configs/yolox/BINARY_yolox_x_8x8_300e_coco.py'
CHECKPOINT_PATH = 'data/pretrain/yolox_x_8x8_300e_coco_20211126_140254-1ef88d67.pth'

cfg = Config.fromfile(CONFIG_FILE)

# replace the ${key} with the value of cfg.key
cfg = replace_cfg_vals(cfg)
cfg.max_epochs = 20
# update data root according to MMDET_DATASETS
update_data_root(cfg)


# set multi-process settings
setup_multi_processes(cfg)


# work_dir is determined in this priority: CLI > segment in file > filename

cfg.work_dir = osp.join('./work_dirs', osp.splitext(osp.basename(CONFIG_FILE))[0])
cfg.auto_resume = False
cfg.gpu_ids = [0]
distributed = False

# create work_dir
mmcv.mkdir_or_exist(osp.abspath(cfg.work_dir))
# dump config
cfg.dump(osp.join(cfg.work_dir, osp.basename(CONFIG_FILE)))
# init the logger before other steps
timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())
log_file = osp.join(cfg.work_dir, f'{timestamp}.log')
logger = get_root_logger(log_file=log_file, log_level=cfg.log_level)

# init the meta dict to record some important information such as
# environment info and seed, which will be logged
meta = dict()
# log env info
env_info_dict = collect_env()
env_info = '\n'.join([(f'{k}: {v}') for k, v in env_info_dict.items()])
dash_line = '-' * 60 + '\n'
logger.info('Environment info:\n' + dash_line + env_info + '\n' +
            dash_line)
meta['env_info'] = env_info
meta['config'] = cfg.pretty_text
# log some basic info
logger.info(f'Distributed training: {distributed}')
logger.info(f'Config:\n{cfg.pretty_text}')

cfg.device = get_device()
# set random seeds
seed = init_random_seed(300, device=cfg.device)
logger.info(f'Set random seed to {seed}, '
            f'deterministic: {False}')
set_random_seed(seed, deterministic=False)
cfg.seed = seed
meta['seed'] = seed
meta['exp_name'] = osp.basename(CONFIG_FILE)

model = init_detector(cfg, CHECKPOINT_PATH, device='cuda:0')
datasets = [build_dataset(cfg.data.train)]
if len(cfg.workflow) == 2:
    assert 'val' in [mode for (mode, _) in cfg.workflow]
    val_dataset = copy.deepcopy(cfg.data.val)
    val_dataset.pipeline = cfg.data.train.get(
        'pipeline', cfg.data.train.dataset.get('pipeline'))
    datasets.append(build_dataset(val_dataset))
if cfg.checkpoint_config is not None:
    # save mmdet version, config file content and class names in
    # checkpoints as meta data
    cfg.checkpoint_config.meta = dict(
        mmdet_version=__version__ + get_git_hash()[:7],
        CLASSES=datasets[0].CLASSES)
# add an attribute for visualization convenience
model.CLASSES = datasets[0].CLASSES

train_detector(
    model,
    datasets,
    cfg,
    distributed=distributed,
    validate=False,
    timestamp=timestamp,
    meta=meta)

model_dict = model.state_dict()    
import torch
torch.save(model_dict,"/content/drive/MyDrive/BINARY_ESG/data/pretrain.pth")
torch.save(model_dict,"../../../content/drive/MyDrive/BINARY_ESG/data/pretrain.pth")