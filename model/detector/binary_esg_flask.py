import json
import numpy as np
from cv2 import VideoCapture, imwrite, resize
from os import path, makedirs
from os.path import isdir
from mmdet.apis import init_detector, inference_detector
from flask import Flask, jsonify, request
import os
from collections import Counter
import time
CONFIG_FILE = 'configs/focalnet/focalnet_binary_tiny_sparse_rcnn.py'
CHECKPOINT_PATH = 'data/pretrain/focal_sparse_rcnn_epoch_17.pth'
ROOT = 'data/binary/cctv_esg'
NUM_SEAT = 6
NUM_FRAME = 7

model = init_detector(CONFIG_FILE, CHECKPOINT_PATH, device='cuda:0')  # or device='cuda:0'
binary_esg_flask = Flask(__name__)

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


@binary_esg_flask.route('/predict')
def predict():
    
    print("start predcit")
    start_time = time.time()
    cctv_img = []
    print("load cctv")
    if not os.path.isfile('data/binary/cctv_esg/cctv.mp4'):
        print("no cctv video")
        return json.dumps({'status': ["None","None","None","None","None","None"]})
    vidcap = VideoCapture('data/binary/cctv_esg/cctv.mp4')
    while 1:
        success,image = vidcap.read()
        if not success:
            break    
        cctv_img.append(resize(image,(640,640)))
    
    cctv_img = np.split(np.array(cctv_img)[:-(len(cctv_img)%NUM_FRAME)],NUM_FRAME)
    imgs = []
    for i in range(NUM_FRAME) :
        imgs.append(cctv_img[i][-1])
        imwrite('check%d.png'%i,imgs[i])
    del cctv_img

    #img_name = os.listdir(ROOT)
    #imgs = [os.path.join(ROOT,img) for img in img_name if 'png' in img or 'jpg' in img]

    print("inference detector")   
    results = inference_detector(model, imgs)

    print("NMS")
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
    
    seats = [[] for _ in range(NUM_SEAT)]
    for box in bbox :
        for i in range(0, NUM_SEAT, 2) :
            if box[i][0] > box[i+1][0] :
                seats[i].append(int(box[i][5]))
                seats[i+1].append(int(box[i+1][5]))
            else :
                seats[i].append(int(box[i+1][5]))
                seats[i+1].append(int(box[i][5]))
    
    status_list = ['EMPTY', 'AWAY', 'FULL']
    final_seat = {'status': []}
    for seat in seats :
        final_seat['status'].append(status_list[Counter(seat).most_common(n=1)[0][0]])
        
    # return info: {'status' : ['EMPTY', 'FULL', 'AWAY', …] #seat}
    
    
    '''  
    import cv2
    img = cv2.imread(imgs[0])
    colors = [(0,0,0),(0,255,0),(0,255,255),(0,0,255)]
    for box in bbox[0]:
        xmin, ymin, xmax, ymax, _, cls = map(int, box)
        cv2.rectangle(img, (xmin, ymin),(xmax,ymax),colors[cls+1])
    pdb.set_trace()
    cv2.imwrite('check.png',img)
    '''
    
    rst = json.dumps(final_seat)
    print(rst)
    end_time = time.time()
    print('in %.4fsec'%(end_time - start_time))
    return rst
if __name__ == '__main__':    
    binary_esg_flask.run('0.0.0.0')