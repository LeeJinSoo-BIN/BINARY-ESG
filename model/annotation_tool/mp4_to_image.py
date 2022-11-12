import cv2
vidcap = cv2.VideoCapture('cctv.mp4')

count = 0
frame = 5
while 1:
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  if not success :
    break
  if count % frame == 0 :
    cv2.imwrite("./path_output_frame/%06d.png" % count, cv2.resize(image,(800,480)))            
  count += 1
    

print("finish! convert video to frame")