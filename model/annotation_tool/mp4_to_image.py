from cv2 import VideoCapture, imwrite, resize
vidcap = VideoCapture('cctv.mp4')
from os import path, makedirs
from os.path import isdir


path = './path_output_frame'
if not isdir(path):
  makedirs(path)

count = 0
frame = 5
while 1:
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  if not success :
    break
  if count % frame == 0 :
    imwrite("./path_output_frame/%06d.png" % count, resize(image,(640,640)))            
  count += 1
    

print("finish! convert video to frame")