# Copyright (c) OpenMMLab. All rights reserved.
import copy
import os.path as osp
import time

import mmcv
from mmcv import Config
from mmcv.runner import get_dist_info, init_dist
from mmcv.utils import get_git_hash

from mmdet import __version__
from mmdet.apis import init_random_seed, set_random_seed, train_detector
from mmdet.datasets import build_dataset, build_dataloader
from mmdet.models import build_detector
from mmdet.utils import (collect_env, get_device, get_root_logger,
                         replace_cfg_vals, setup_multi_processes,
                         update_data_root)
from mmdet.apis import init_detector, inference_detector, single_gpu_test
import pdb
CONFIG_FILE = 'configs/yolox/yolox_x_8x8_300e_coco.py'
CHECKPOINT_PATH = 'data/pretrain/yolox_x_8x8_300e_coco_20211126_140254-1ef88d67.pth'
#CONFIG_FILE = 'configs/ddod/ddod_r50_fpn_1x_coco.py'
#CHECKPOINT_PATH = 'data/pretrain/ddod_r50_fpn_1x_coco_20220523_223737-29b2fc67.pth'

CONFIG_FILE = 'configs/focalnet/focalnet_binary_tiny_sparse_rcnn.py'
CHECKPOINT_PATH = 'work_dirs/full/focalnet_binary_tiny_sparse_rcnn/epoch_17.pth'


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



    pdb.set_trace()
    cfg.model.train_cfg = None
    model = build_detector(cfg.model, test_cfg=cfg.get('test_cfg'))

    pdb.set_trace()
    datasets = build_dataset(cfg.data.test)


    test_dataloader_default_args = dict(
        samples_per_gpu=1,
        workers_per_gpu=2,
        dist=distributed,
        shuffle=False)    
    test_loader_cfg = {
        **test_dataloader_default_args,
        **cfg.data.get('test_dataloader', {})
    }

    data_loader = build_dataloader(datasets, **test_loader_cfg)

    '''
    train_dataloader_default_args = dict(
        samples_per_gpu=2,
        workers_per_gpu=1,
        # `num_gpus` will be ignored if distributed
        num_gpus=len(cfg.gpu_ids),
        dist=distributed,
        seed=cfg.seed,
        persistent_workers=False)

    train_loader_cfg = {
        **train_dataloader_default_args,
        **cfg.data.get('train_dataloader', {})
    }

    data_loader = build_dataloader(datasets, **train_loader_cfg)
    '''
    results = single_gpu_test(model, data_loader, show= True, out_dir=cfg.work_dir)
    pdb.set_trace()


    '''or img, 
    model.module.show_result(
                    img_show,
                    result[i],
                    bbox_color=PALETTE,
                    text_color=PALETTE,
                    mask_color=PALETTE,
                    show=show,
                    out_file=out_file,
                    score_thr=show_score_thr)
    '''


    if rank == 0:
        if args.out:
            print(f'\nwriting results to {args.out}')
            mmcv.dump(outputs, args.out)
        kwargs = {} if args.eval_options is None else args.eval_options
        if args.format_only:
            dataset.format_results(outputs, **kwargs)
        if args.eval:
            eval_kwargs = cfg.get('evaluation', {}).copy()
            # hard-code way to remove EvalHook args
            for key in [
                    'interval', 'tmpdir', 'start', 'gpu_collect', 'save_best',
                    'rule', 'dynamic_intervals'
            ]:
                eval_kwargs.pop(key, None)
            eval_kwargs.update(dict(metric=args.eval, **kwargs))
            metric = dataset.evaluate(outputs, **eval_kwargs)
            print(metric)
            metric_dict = dict(config=args.config, metric=metric)
            if args.work_dir is not None and rank == 0:
                mmcv.dump(metric_dict, json_file)




if __name__ == '__main__':
    main()
