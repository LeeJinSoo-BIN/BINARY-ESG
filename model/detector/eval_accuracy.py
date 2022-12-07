import json
import numpy as np
from mmdet.apis import init_detector, inference_detector
import os
from collections import Counter
CONFIG_FILE = 'configs/focalnet/focalnet_binary_tiny_sparse_rcnn.py'
CHECKPOINT_PATH = 'data/pretrain/focal_sparse_rcnn_epoch_17.pth'
ROOT = 'data/binary/test_esg'
TEST_JSON = 'data/binary/annotations/binary_esg_test_full.json'
NUM_SEAT = 6
model = init_detector(CONFIG_FILE, CHECKPOINT_PATH, device='cuda:0')  # or device='cuda:0'


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



def eval():
    
    with open(TEST_JSON) as f:
        gt_dict = json.load(f)
    
    imgs = []
    gts = []
    image_dict = {}
    for img in gt_dict["class_of_seat"] :
        image_dict.update({img['image_id'] : img['class']})
    for img in gt_dict["images"] :
        imgs.append(os.path.join(ROOT,img["file_name"]))
        gts.append(image_dict[img["id"]])

    import pdb; pdb.set_trace()

    results = inference_detector(model, imgs)
    new_results = [[] for _ in range(len(results))]
    pdb.set_trace()
    for num in range(len(results)):      
        for i in range(3):
            for j in range(len(results[num][i])):
                new_results[num].append(np.append(results[num][i][j], np.array([i])))
        
    pdb.set_trace()
    bbox = []
    for i in range(len(results)):
        bbox.append(nms(new_results[i], 0.15, 0.1))
    print(len(bbox)) # debugging
    
    pdb.set_trace()
    for i in range(len(bbox)):
        bbox[i].sort( key=lambda x:-x[3])
    



    pdb.set_trace()
    new_bbox = [[] for _ in range(len(results))]
    for j, box in enumerate(bbox) :
        for i in range(0, NUM_SEAT, 2) :
            if box[i+1][0] > box[i][0] :
                new_bbox[j].append(int(box[i+1][5]+1))
                new_bbox[j].append(int(box[i][5]+1))
            else :
                new_bbox[j].append(int(box[i][5]+1))
                new_bbox[j].append(int(box[i+1][5]+1))
    
    #status_list = ['EMPTY', 'AWAY', 'FULL']
    import pdb; pdb.set_trace()
    total = len(results)*NUM_SEAT
    correct = 0
    gts = np.array(gts)
    new_bbox = np.array(new_bbox)
    for gt, predict in zip(gts, new_bbox) :
        correct+= sum(gt == predict)
    
    print("Accuracy : ", correct/total )
        
        
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
    
    
if __name__ == '__main__':  
    eval()