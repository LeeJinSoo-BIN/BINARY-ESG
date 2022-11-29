import os
data_root = "./../total_esg"
import numpy as np

import pdb; pdb.set_trace()
imgs = np.array(os.listdir(data_root))
valid_idx = np.random.choice(len(imgs), 118, replace=False)
valid_imgs = imgs[valid_idx]
train_imgs = []
for img in imgs :
    if not img in valid_imgs :
        train_imgs.append(img)
import pdb; pdb.set_trace()

for i, file in enumerate(train_imgs):
    filename = os.path.join(data_root,file)
    newfilename = os.path.join(data_root,"binary_esg_train_image%04d.png"%(i+1))
    os.rename(filename, newfilename)

for i, file in enumerate(valid_imgs):
    filename = os.path.join(data_root,file)
    newfilename = os.path.join(data_root,"binary_esg_valid_image%04d.png"%(i+1))
    os.rename(filename, newfilename)