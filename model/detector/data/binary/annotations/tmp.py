import json


with open('binary_esg_train.json') as f:
    json_object = json.load(f)

import pdb; pdb.set_trace()
'''
new_annotations = []
for ann in json_object['annotations'] :
    ann.pop('segmentation')
    new_annotations.append(ann)


json_object['annotations'] = new_annotations
with open('binary_esg_train.json', 'w') as f:
    json.dump(json_object, f, indent=2)
'''


new_images = []
for img in json_object['images'] :
    widht = img.pop('widht')
    img.update({'width' : widht})
    new_images.append(img)


json_object['images'] = new_images
with open('binary_esg_train.json', 'w') as f:
    json.dump(json_object, f, indent=2)