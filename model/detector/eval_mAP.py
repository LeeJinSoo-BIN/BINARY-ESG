from mmdet.apis import init_detector, inference_detector, show_result_pyplot
import pdb
import os
import json
import numpy as np

CONFIG_FILE = 'configs/focalnet/focalnet_binary_tiny_sparse_rcnn.py'
CHECKPOINT_PATH = 'data/pretrain/focal_sparse_rcnn_epoch_17.pth'
TEST_JSON = 'data/binary/annotations/binary_esg_train.json'

with open(TEST_JSON) as f:
    test_anno = json.load(f)


model = init_detector(CONFIG_FILE, CHECKPOINT_PATH, device='cuda:0')  # or device='cuda:0'
root = 'data/binary/train_esg'


imgs = [os.path.join(root,img['file_name']) for img in test_anno['images']]



results = []
for img in imgs :   

    result = inference_detector(model, img)
    results.append(result)
import pdb; pdb.set_trace()
new_results = [[] for _ in range(len(results))]
for num in range(len(results)):      
    for i in range(3):
        for j in range(len(results[num][i])):
            new_results[num].append(np.append(results[num][i][j], np.array([i])))


res = []
for img, result in zip(test_anno['images'], new_results) :
    
    for xmin, ymin, xmax, ymax, score, cat in result:
        res.append({
            "image_id" : img['id'],
            "category_id" : int(cat),
            "bbox" : [xmin, ymin, xmax-xmin, ymax - ymin],
            "score" : score
            })
    



from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval


import pdb; pdb.set_trace()
coco_gt = COCO(TEST_JSON)
coco_pred = coco_gt.loadRes(res)

coco_eval = COCOeval(coco_gt, coco_pred, 'bbox')
coco_eval.evaluate()
coco_eval.accumulate()
coco_eval.summarize()
import pdb; pdb.set_trace()