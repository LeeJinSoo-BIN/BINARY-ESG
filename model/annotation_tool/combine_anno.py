import json
json1 = '/home/jslee/workspace/BINARY-ESG/model/detector/data/binary/annotations/binary_esg_val_image_annotations.json'
json2 = '/home/jslee/workspace/BINARY-ESG/model/detector/data/binary/annotations/binary_esg_test.json'
output_json = 'train_esg_test_full.json'

with open(json1) as f:
    json_object1 = json.load(f)

max_img_id = 0
max_ann_id = 0
for img in json_object1['images'] :
    if max_img_id < img['id'] :
        max_img_id = img['id']

for img in json_object1['annotations'] :
    if max_ann_id < img['id'] :
        max_ann_id = img['id']

with open(json2) as f:
    json_object2 = json.load(f)

max_img_id += 1
max_ann_id += 1
for img in json_object2['images'] :
    img['id']+= max_img_id

for img in json_object2['annotations'] :
    img['id']+= max_ann_id
    img['image_id']+= max_img_id

for img in json_object2['class_of_seat'] :
    img['image_id']+= max_img_id

img_list = json_object1['images']
img_list.extend(json_object2['images'])

ann_list = json_object1['annotations']
ann_list.extend(json_object2['annotations'])

cls_list = json_object1["class_of_seat"]
cls_list.extend(json_object2["class_of_seat"])

import pdb; pdb.set_trace()
new_json_object ={
    "info":{
        "num of images" : json_object1['info']['num of images'] + json_object2['info']['num of images'],
        "num of objects" : json_object1['info']['num of objects'] + json_object2['info']['num of objects']
    },
    "images" : img_list,
    "annotations" : ann_list,
    "categories" : json_object1["categories"],
    "class_of_seat" : cls_list
}

with open(output_json, 'w') as f:
    json.dump(new_json_object, f, indent=2)

