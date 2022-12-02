from mmdet.apis import init_detector, inference_detector
from flask import Flask, jsonify, request

CONFIG_FILE = 'configs/focalnet/focalnet_binary_tiny_sparse_rcnn.py'
CHECKPOINT_PATH = 'data/pretrain/focal_sparse_rcnn_epoch_17.pth'

model = init_detector(CONFIG_FILE, CHECKPOINT_PATH, device='cpu')  # or device='cuda:0'
imgs = ['data/binary/cctv_esg/test_001.jpg','data/binary/cctv_esg/test_002.jpg','data/binary/cctv_esg/test_003.jpg']
results = inference_detector(model, imgs)

binary_esg_flask = Flask(__name__)
@binary_esg_flask.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        #img_bytes = request.input_stream.read()
        print("check\n")
        class_id, class_name = get_prediction(image_bytes=img_bytes)
        print(class_id, class_name)
        return jsonify({'class_id': class_id, 'class_name': class_name})
        #return "hello"


if __name__ == '__main__':
    binary_esg_flask.run()
