from mmdet.apis import init_detector, inference_detector, show_result_pyplot
import torch, gc
gc.collect()
torch.cuda.empty_cache()
config_file = 'yolov3_mobilenetv2_320_300e_coco.py'
checkpoint_file = 'yolov3_mobilenetv2_320_300e_coco_20210719_215349-d18dff72.pth'

config_file = 'configs/convnext/cascade_mask_rcnn_convnext-s_p4_w7_fpn_giou_4conv1f_fp16_ms-crop_3x_coco.py'
checkpoint_file ='cascade_mask_rcnn_convnext-s_p4_w7_fpn_giou_4conv1f_fp16_ms-crop_3x_coco_20220510_201004-3d24f5a4.pth'
model = init_detector(config_file, checkpoint_file, device='cuda:0')  # or device='cuda:0'
gc.collect()
torch.cuda.empty_cache()
import cv2
img = cv2.imread('demo/demo2.jpg')
import pdb; pdb.set_trace()
result = inference_detector(model, 'demo/demo2.jpg')

img_ori = img.copy()
colors = []
for i, classes in enumerate(result) :
    
    for d_object in classes :
        img = cv2.rectangle(img,(int(d_object[0]),int(d_object[1])), (int(d_object[2]),int(d_object[3])),(255,255,0))

cv2.imwrite("wow.png",img)
show_result_pyplot(model,img_ori,result,score_thr=0.2)