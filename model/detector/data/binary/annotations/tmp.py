import json


with open('instances_train_esg.json') as f:
    json_object = json.load(f)

import pdb; pdb.set_trace()

new_annotations = []
for ann in json_object['annotations'] :
    ann.pop('segmentation')
    new_annotations.append(ann)


json_object['annotations'] = new_annotations
with open('binary_esg_train.json', 'w') as f:
    json.dump(json_object, f, indent=2)
