import torch
#from mmdet.apis import init_detector, inference_detector, show_result_pyplot


CONFIG_FILE = 'configs/yolox/BINARY_yolox_x_8x8_300e_coco.py'
CHECKPOINT_PATH1 = 'work_dirs/BINARY_yolox_x_8x8_300e_coco/epoch_30.pth'
CHECKPOINT_PATH2 = 'data/pretrain/yolox_x_8x8_300e_coco_20211126_140254-1ef88d67.pth'


epo = torch.load(CHECKPOINT_PATH1)
pre = torch.load(CHECKPOINT_PATH2)
es = epo['state_dict']
ps = pre['state_dict']
pdb.set_trace()

eks = es.keys()

pdb.set_trace()
new_dict = { ek:ev for ek,ev in es.items() if not("ema" in ek )}
    
        








pdb.set_trace()
model = init_detector(CONFIG_FILE, CHECKPOINT_PATH, device='cuda:0')


result = inference_detector(model, 'data/binary/train_esg/binary_esg_train_image0001.png')

