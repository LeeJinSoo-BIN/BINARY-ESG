import json


def xyxy_to_xywh(anno_dict):
    #xywh = []
    xyxy = anno_dict["annotations"]    
    for anno in xyxy:
        xmin,ymin, xmax,ymax = anno["bbox"]
        w = xmax - xmin
        h = ymax - ymin
        anno["bbox"] = [xmin, ymin, w, h]
    return anno_dict

def xywh_to_xyxy(anno_dict):
    #xywh = []
    xywh = anno_dict["annotations"]    
    for anno in xywh:
        xmin,ymin, w,h = anno["bbox"]
        xmax = xmin + w
        ymax = ymin + h
        anno["bbox"] = [xmin, ymin, xmax, ymax]
    return anno_dict
    
input_json = 'train_esg_annotations_no.json'
output_json = 'train_esg_annotations_yes.json'
with open(input_json) as f:
    json_object = json.load(f)

#new_json_object = xyxy_to_xywh(json_object)
new_json_object = xywh_to_xyxy(json_object)
nnew_json_object = xyxy_to_xywh(new_json_object)

with open(output_json, 'w') as f:
    json.dump(nnew_json_object, f, indent=2)



