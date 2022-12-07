# Copyright (c) OpenMMLab. All rights reserved.
import copy
import os.path as osp
import time
import os
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
import mmcv
from mmcv import Config
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
import pdb
CONFIG_FILE = 'configs/yolox/yolox_x_8x8_300e_coco.py'
CHECKPOINT_PATH = 'data/pretrain/yolox_x_8x8_300e_coco_20211126_140254-1ef88d67.pth'
#CONFIG_FILE = 'configs/ddod/ddod_r50_fpn_1x_coco.py'
#CHECKPOINT_PATH = 'data/pretrain/ddod_r50_fpn_1x_coco_20220523_223737-29b2fc67.pth'

CONFIG_FILE = 'configs/focalnet/focalnet_binary_tiny_sparse_rcnn.py'
CHECKPOINT_PATH = 'data/pretrain/focalnet_tiny_lrf_sparsercnn_3x.pth'


def main():       
    
    cfg = Config.fromfile(CONFIG_FILE)
    # replace the ${key} with the value of cfg.key
    cfg = replace_cfg_vals(cfg)

    # update data root according to MMDET_DATASETS
    update_data_root(cfg)


    # set multi-process settings
    setup_multi_processes(cfg)


    # work_dir is determined in this priority: CLI > segment in file > filename
    cfg.work_dir = osp.join('./work_dirs/full', osp.splitext(osp.basename(CONFIG_FILE))[0])
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
    #model = build_detector(cfg.model, train_cfg=cfg.get('train_cfg'), test_cfg=cfg.get('test_cfg'))
    
    datasets = [build_dataset(cfg.data.train)]
    #import pdb; pdb.set_trace()
    cfg.workflow = [('train',1),('val',1)]
    if len(cfg.workflow) == 2:       
        datasets.append(build_dataset(cfg.data.val))
    if cfg.checkpoint_config is not None:
        # save mmdet version, config file content and class names in
        # checkpoints as meta data
        cfg.checkpoint_config.meta = dict(
            #mmdet_version=__version__ + get_git_hash()[:7],
            CLASSES=datasets[0].CLASSES)
    # add an attribute for visualization convenience
    model.CLASSES = datasets[0].CLASSES

    pdb.set_trace()
    train_detector(
        model,
        datasets,
        cfg,
        distributed=distributed,
        validate=True
        timestamp=timestamp,
        meta=meta)





if __name__ == '__main__':
    main()
