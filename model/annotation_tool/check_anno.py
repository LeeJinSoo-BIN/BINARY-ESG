import json
from collections import defaultdict
import os
import cv2
img_data_root = './../train_esg'
input_json = 'binary_esg_train_check_xyxy.json'
output_path = './../train_esg_check'
if not os.path.isdir(output_path):
    os.makedirs(output_path)

with open(input_json) as f:
    json_dict = json.load(f)

def createIndex(json_dict):
    # create index
    print('creating index...')
    anns, cats, imgs = {}, {}, {}
    imgToAnns,catToImgs = defaultdict(list),defaultdict(list)
    if 'annotations' in json_dict:
        for ann in json_dict['annotations']:
            imgToAnns[ann['image_id']].append(ann)
            anns[ann['id']] = ann

    if 'images' in json_dict:
        for img in json_dict['images']:
            imgs[img['id']] = img

    if 'categories' in json_dict:
        for cat in json_dict['categories']:
            cats[cat['id']] = cat

    if 'annotations' in json_dict and 'categories' in json_dict:
        for ann in json_dict['annotations']:
            catToImgs[ann['category_id']].append(ann['image_id'])

    print('index created!')

    # create class members
    return anns, imgToAnns, catToImgs, cats
    
anns, imgToAnns, catToImgs, cats = createIndex(json_dict)
colors = [(255,255,255), (0,255,0),(0,255,255),(0,0,255)]
import pdb; pdb.set_trace()
for img in json_dict['images']:
    ann = imgToAnns[img['id']]
    file_name = img['file_name']
    img_path = os.path.join(img_data_root, file_name)
    img_data = cv2.imread(img_path)
    for box in ann :
        xmin,ymin,xmax,ymax = box['bbox']
        cat = box['category_id']
        img_data = cv2.rectangle(img_data,(xmin,ymin),(xmax,ymax),colors[cat])
    img_out_path = os.path.join(output_path, file_name)
    cv2.imwrite(img_out_path, img_data)
print("done")
