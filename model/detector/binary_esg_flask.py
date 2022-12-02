import json
import numpy as np
from mmdet.apis import init_detector, inference_detector
from flask import Flask, jsonify, request
import os
CONFIG_FILE = 'configs/focalnet/focalnet_binary_tiny_sparse_rcnn.py'
CHECKPOINT_PATH = 'data/pretrain/focal_sparse_rcnn_epoch_17.pth'
ROOT = 'data/binary/cctv_esg'
model = init_detector(CONFIG_FILE, CHECKPOINT_PATH, device='cuda:0')  # or device='cuda:0'

#binary_esg_flask = F1lask(__name__)

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




#@binary_esg_flask.route('/predict')
def predict():
    
    
    img_name = os.listdir(ROOT)
    imgs = [os.path.join(ROOT,img) for img in img_name if 'png' in img or 'jpg' in img]
    results = inference_detector(model, imgs)
    new_results = [[] for num in range(len(results))]
    import pdb; pdb.set_trace()
    for num in range(len(results)):      
        for i in range(3):
            for j in range(len(results[i])):
                new_results[num].append(np.append(results[num][i][j], np.array([i])))
    import pdb; pdb.set_trace()
    bbox = []
    for i in range(len(results)):
        bbox.append(nms(new_results[i], 0.15, 0.2))
    print(len(bbox)) # debugging


    status_list = ['EMPTY', 'AWAY', 'FULL']
    json_list = {'status': []}
    # return info: {'status' : ['EMPTY', 'FULL', 'AWAY', …]}
    '''
    {
        '1' : 'EMPTY',
        '2' : 'NONE',
        ...
        '6' : 'AWAY'
    }
    '''
    for seat in sorted(new_results[0], key=lambda x:((x[3] - x[1] / 2), (x[2] - x[0]) / 2)):
        json_list['status'].append(status_list[int(seat[5])])
    
    return json.dumps(json_list)


if __name__ == '__main__':
    predict()
    #binary_esg_flask.run()
