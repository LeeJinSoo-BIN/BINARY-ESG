import json
from collections import defaultdict
import os
import cv2
img_data_root = './../train_esg'
input_json = 'binary_esg_train.json'
output_path = './../train_esg_check'
if not os.path.isdir(output_path):
    os.makedirs(output_path)

with open(input_json) as f:
    json_dict = json.load(f)


categories = {cat["name"] : 0 for cat in json_dict['categories']}
categories_key = {cat["id"] : cat["name"] for cat in json_dict['categories']}

import pdb; pdb.set_trace()
for ob in json_dict['annotations'] :
    categories[categories_key[ob['category_id']]] += 1

print(categories)