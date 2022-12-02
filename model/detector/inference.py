from mmdet.apis import init_detector, inference_detector, show_result_pyplot
import torch, gc
import pdb
import os
gc.collect()
torch.cuda.empty_cache()
config_file = 'yolov3_mobilenetv2_320_300e_coco.py'
checkpoint_file = 'yolov3_mobilenetv2_320_300e_coco_20210719_215349-d18dff72.pth'

config_file = 'configs/convnext/cascade_mask_rcnn_convnext-s_p4_w7_fpn_giou_4conv1f_fp16_ms-crop_3x_coco.py'
checkpoint_file ='cascade_mask_rcnn_convnext-s_p4_w7_fpn_giou_4conv1f_fp16_ms-crop_3x_coco_20220510_201004-3d24f5a4.pth'


config_file = 'configs/ddod/ddod_r50_fpn_1x_coco.py'
checkpoint_file = 'ddod_r50_fpn_1x_coco_20220523_223737-29b2fc67.pth'

CONFIG_FILE = 'configs/yolox/BINARY_yolox_x_8x8_300e_coco.py'
CHECKPOINT_PATH = 'work_dirs/full/BINARY_yolox_x_8x8_300e_coco/epoch_275.pth'




CONFIG_FILE = 'configs/focalnet/focalnet_binary_tiny_sparse_rcnn.py'
CHECKPOINT_PATH = 'data/pretrain/focal_sparse_rcnn_epoch_17.pth'

model = init_detector(CONFIG_FILE, CHECKPOINT_PATH, device='cpu')  # or device='cuda:0'
imgs = ['data/binary/train_esg/binary_esg_train_image0100.png','data/binary/train_esg/binary_esg_train_image0030.png','data/binary/train_esg/binary_esg_train_image0050.png']
root = 'data/binary/test_esg'
#img_name = os.listdir(root)
#imgs = [os.path.join(root,img) for img in img_name]
results = inference_detector(model, imgs)

folder = "work_dirs/debug/" +CONFIG_FILE.split('/')[-1][:-3]
if not os.path.isdir(folder):
    os.makedirs(folder)

import cv2

colors = [(0,0,0),(0,255,0),(0,255,255),(0,0,255)]
thres_hold = [0.0, 0.2, 0.3 ,0.4, 0.5, 0.6]
imglists = []
for _, (img_path, result) in enumerate(zip(imgs, results)) :    
    img = cv2.imread(img_path)
    imglist = [img.copy() for _ in range(len(thres_hold))]
    for i, classes in enumerate(result):
        if i == 0 :
            color_ = (0,255,0)
        elif i == 1:
            color_ = (0,255,255)
        elif i == 2:
            color_ = (0,0,255)
        for ii, th in enumerate(thres_hold):
            for d_object in classes :
                if d_object[4] > th :                
                    imglist[ii] = cv2.rectangle(imglist[ii], (int(d_object[0]),int(d_object[1])), (int(d_object[2]),int(d_object[3])), color_)
    imglists.append(imglist)        



for i, img_path in enumerate(imgs):
    img_name = img_path.split('/')[-1]    
    for ii, img in enumerate(imglists[i]) :      
        cv2.imwrite(folder+'/'+img_name[:-4]+"th"+str(thres_hold[ii])+".png", img)

#cv2.imwrite("wow.png",img)
#show_result_pyplot(model,imgs,results,score_thr=0.3)