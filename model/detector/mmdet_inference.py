from mmdet.apis import init_detector, inference_detector, show_result_pyplot
import torch, gc
gc.collect()
torch.cuda.empty_cache()
config_file = 'yolov3_mobilenetv2_320_300e_coco.py'
checkpoint_file = 'yolov3_mobilenetv2_320_300e_coco_20210719_215349-d18dff72.pth'

config_file = 'configs/convnext/cascade_mask_rcnn_convnext-s_p4_w7_fpn_giou_4conv1f_fp16_ms-crop_3x_coco.py'
checkpoint_file ='cascade_mask_rcnn_convnext-s_p4_w7_fpn_giou_4conv1f_fp16_ms-crop_3x_coco_20220510_201004-3d24f5a4.pth'


config_file = 'configs/ddod/ddod_r50_fpn_1x_coco.py'
checkpoint_file = 'ddod_r50_fpn_1x_coco_20220523_223737-29b2fc67.pth'


model = init_detector(config_file, checkpoint_file, device='cuda:0')  # or device='cuda:0'
gc.collect()
torch.cuda.empty_cache()
import cv2
img = cv2.imread('demo/demo3.png')

result = inference_detector(model, 'demo/demo3.png')

img_ori = img.copy()
colors = []
#show_class_list = {'person':0, 'bench':13,'backpack':24,'handbag':26,'dining table':60}
show_class_list = [0,60]
#for i, class_ in enumerate(model.CLASSES):
    #print(i, class_)
thres_hold = [0.1, 0.2 ,0.3]
import pdb; pdb.set_trace()

img_th_01 = img.copy()
img_th_02 = img.copy()
img_th_03 = img.copy()
imglist = [img_th_01,img_th_02,img_th_03]
for i, classes in enumerate(result) :
    if i in show_class_list :
        if i == 0 :
            color_ = (255,0,0)
        elif i == 60:
            color_ = (0,255,0)


        for ii, th in enumerate(thres_hold):
            for d_object in classes :
                if d_object[4] > th :                
                    imglist[ii] = cv2.rectangle(imglist[ii], (int(d_object[0]),int(d_object[1])), (int(d_object[2]),int(d_object[3])), color_)
            

for i in range(3):
    cv2.imwrite("th"+str(thres_hold[i])+".png", imglist[i])


#cv2.imwrite("wow.png",img)
#show_result_pyplot(model,img_ori,result,score_thr=0.3)