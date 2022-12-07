import json


input_json = '../detector/data/binary/annotations/binary_esg_test.json'
with open(input_json) as f:
    json_dict = json.load(f)


for anno in json_dict['annotations'] :
    _,_,w,h = anno['bbox']
    anno['area'] = float(w*h)

output_json = '../detector/data/binary/annotations/binary_esg_test.json'
with open(output_json, 'w') as f:
    json.dump(json_dict, f, indent=2)
