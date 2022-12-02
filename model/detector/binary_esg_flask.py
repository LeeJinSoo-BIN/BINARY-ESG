from mmdet.apis import init_detector, inference_detector
from flask import Flask, jsonify, request

CONFIG_FILE = 'configs/focalnet/focalnet_binary_tiny_sparse_rcnn.py'
CHECKPOINT_PATH = 'data/pretrain/focal_sparse_rcnn_epoch_17.pth'

model = init_detector(CONFIG_FILE, CHECKPOINT_PATH, device='cpu')  # or device='cuda:0'


binary_esg_flask = Flask(__name__)
@binary_esg_flask.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        imgs = ['data/binary/cctv_esg/test_001.jpg','data/binary/cctv_esg/test_002.jpg','data/binary/cctv_esg/test_003.jpg']
        results = inference_detector(model, imgs)
        return results
if __name__ == '__main__':
    binary_esg_flask.run()
