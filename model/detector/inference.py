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

model = init_detector(CONFIG_FILE, CHECKPOINT_PATH, device='cuda:0')  # or device='cuda:0'
root = 'data/binary/test_esg'
img_name = os.listdir(root)
imgs = [os.path.join(root,img) for img in img_name if 'md' not in img]
import pdb; pdb.set_trace()
results = inference_detector(model, imgs)

folder = "work_dirs/debug/" +CONFIG_FILE.split('/')[-1][:-3]
if not os.path.isdir(folder):
    os.makedirs(folder)

# import cv2
# import pdb; pdb.set_trace()
# colors = [(0,0,0),(0,255,0),(0,255,255),(0,0,255)]
# thres_hold = [0.0, 0.2, 0.3 ,0.4, 0.5, 0.6]
# imglists = []
# for _, (img_path, result) in enumerate(zip(imgs, results)) :    
#     img = cv2.imread(img_path)
#     imglist = [img.copy() for _ in range(len(thres_hold))]
#     for i, classes in enumerate(result):
#         if i == 0 :
#             color_ = (0,255,0)
#         elif i == 1:
#             color_ = (0,255,255)
#         elif i == 2:
#             color_ = (0,0,255)
#         for ii, th in enumerate(thres_hold):
#             for d_object in classes :
#                 if d_object[4] > th :                
#                     imglist[ii] = cv2.rectangle(imglist[ii], (int(d_object[0]),int(d_object[1])), (int(d_object[2]),int(d_object[3])), color_)
#     imglists.append(imglist)        


# import pdb; pdb.set_trace()
# for i, img_path in enumerate(imgs):
#     img_name = img_path.split('/')[-1]    
#     for ii, img in enumerate(imglists[i]) :      
#         cv2.imwrite(folder+'/'+img_name[:-4]+"th"+str(thres_hold[ii])+".png", img)

#cv2.imwrite("wow.png",img)
#show_result_pyplot(model,imgs,results,score_thr=0.3)


# #### jeongmin - nms

def bb_intersection_over_union(boxA, boxB):
   xA = max(boxA[0], boxB[0])
   yA = max(boxA[1], boxB[1])
   xB = min(boxA[2], boxB[2])
   yB = min(boxA[3], boxB[3])
   
   interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

   boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
   boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

   iou = interArea / float(boxAArea + boxBArea - interArea)

   return iou

def nms(bboxes, iou_threshold, threshold=0):

    # box 점수가 threshold보다 높은 것을 선별합니다.
    bboxes = [box for box in bboxes if box[4] > threshold]
   
    # 정렬
    bboxes = sorted(bboxes, key=lambda x: -x[4])
    bboxes_after_nmn = []

    while bboxes:
        chosen_box = bboxes.pop(0)
        bboxes = [box for box in bboxes if bb_intersection_over_union(chosen_box, box) < iou_threshold]
        bboxes_after_nmn.append(chosen_box)

    return bboxes_after_nmn


import numpy as np
new_results = [[] for _ in range(len(results))]

for num in range(len(results)):      
    for i in range(3):
        for j in range(len(results[num][i])):
            new_results[num].append(np.append(results[num][i][j], np.array([i])))
    

bbox = []
for i in range(len(results)):
    bbox.append(nms(new_results[i], 0.15, 0.1))
print(len(bbox)) # debugging


for i in range(len(bbox)):
    bbox[i].sort( key=lambda x:-x[3])


folder = "work_dirs/debug/" +CONFIG_FILE.split('/')[-1][:-3] + "_nms"
if not os.path.isdir(folder):
    os.makedirs(folder)

import cv2


colors = [(0,0,0),(0,255,0),(0,255,255),(0,0,255)]
imglists = []
for _, (img_path, result) in enumerate(zip(imgs, bbox)) :      
    img = cv2.imread(img_path)
    imglist = [img.copy() for _ in range(1)]
    i = 0
    for x1, y1, x2, y2, _, ci in result:          
        imglist[i] = cv2.rectangle(imglist[i], (int(x1),int(y1)), (int(x2),int(y2)), colors[int(ci) + 1])
    imglists.append(imglist)        

import pdb; pdb.set_trace()
for i, img_path in enumerate(imgs):
    img_name = img_path.split('/')[-1]    
    for ii, img in enumerate(imglists[i]) :      
        cv2.imwrite(folder+'/'+img_name[:-4]+"_nms"+".png", img)





# seats = [[] for _ in range(NUM_SEAT)]
# for box in bbox :
#     for i in range(0, NUM_SEAT, 2) :
#         if box[i][0] > box[i+1][0] :
#             seats[i].append(int(box[i][5]))
#             seats[i+1].append(int(box[i+1][5]))
#         else :
#             seats[i].append(int(box[i+1][5]))
#             seats[i+1].append(int(box[i][5]))