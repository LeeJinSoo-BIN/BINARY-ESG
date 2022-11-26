import sys
import PyQt5
from PyQt5 import uic
from cv2 import IMREAD_COLOR, imdecode
import os
import numpy as np
from PyQt5.QtCore import Qt, QRect
import sys
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
import json
import datetime



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path("test.ui")
form_class = uic.loadUiType(form)[0]

object_dict = { 1:'Empty', 2:'Away', 3:'Full', 
                'Empty':1, 'Away':2, 'Full':3}

categories = [{
    "id": 1,
    "name": 'Empty',
    "supercategory": 'Empty'
},
{
    "id": 2,
    "name": 'Away',
    "supercategory": 'Away'
},
{
    "id": 3,
    "name": 'Full',
    "supercategory": 'Full'
}]

class BoxLabel(PyQt5.QtWidgets.QLabel):
    def __init__(self,parent):
        super(BoxLabel, self).__init__(parent)
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.flag = False
        self.obj = None
        self.rectangles = []
        
        self.setMouseTracking(True)

        self.ann_ids = 1

    def mousePressEvent(self,event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()
         # 
    def mouseReleaseEvent(self,event):
        self.flag = False
        
        
        if self.obj != None :
            rect = QRect(self.x0, self.y0, self.x1-self.x0, self.y1-self.y0)
            self.rectangles.append((rect, object_dict[self.obj], self.ann_ids))
            self.ann_ids += 1
        self.update()
         # 
    def mouseMoveEvent(self,event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()
         #  event

    
    def select_Qpen(self, obj, type=Qt.SolidLine ):
        
        
        if obj == 1 :            
            return QPen(QColor(0,255,0),Qt.SolidLine)
        elif obj == 2 :
            return QPen(QColor(255,255,0),Qt.SolidLine)
        elif obj == 3 :
            return QPen(QColor(255,0,0),Qt.SolidLine)
        else:
            return QPen(QColor(0,0,0,0),Qt.SolidLine)

    def paintEvent(self, event):
        super(BoxLabel, self).paintEvent(event)
        if self.flag :
            painter = QPainter(self)
            qbox = QPixmap()

            rect = QRect(self.x0, self.y0, self.x1-self.x0, self.y1-self.y0) #x y w h
            
            
            qpen = self.select_Qpen(self.obj)
            painter.setPen(qpen)
            painter.drawRect(rect)
            
            
      
        self.draw_rects()
        

    def draw_rects(self):
        painter = QPainter(self)
        for rect, obj, _ in self.rectangles :            
            qpen = self.select_Qpen(object_dict[obj])
            painter.setPen(qpen)
            painter.drawRect(rect)
        


    def save_rectangle(self, img, img_name, img_id):
        save_info = list()
        currentImageInfo = {
                            "file_name": img_name,
                            "id" : img_id,
                            "height" : img.shape[0],
                            "widht" : img.shape[1]
                            }
                            

        save_info.append(currentImageInfo)

        currentAnnotation = list()
        for rect, obj, ann_id in self.rectangles :
            currentAnnotation.append({
                                    "bbox": [
                                            rect.x(),
                                            rect.y(),
                                            rect.width(),
                                            rect.height()
                                            ],#xmin ymin w h
                                    "category_id" : object_dict[obj],
                                    "image_id" : img_id,
                                    "id" : ann_id,
                                    "iscrowd" : 0
                                    })
        save_info.extend(currentAnnotation)
        self.rectangles = []
        return save_info
        '''
        for rect,obj in self.rectangles :
            img = cv2.rectangle(img, (rect.x(), rect.y()), (rect.height()+rect.x(), rect.width()+rect.y()),(255,0,0))
        cv2.imwrite("test.png",img)
        '''
    
    def load_rectangles(self, save_info):
        
        if save_info != None:
            saved_rect = list()
            print(save_info)
            for x in range(1, len(save_info)):
                print(save_info[x])
                xmin, ymin, w, h = save_info[x]["bbox"]
                rect = QRect(xmin, ymin, w, h)
                ann_id = save_info[x]["id"]
                saved_rect.append((rect, object_dict[save_info[x]["category_id"]], ann_id))
            self.rectangles = saved_rect
        self.update()

    def delete_box(self):
        if len(self.rectangles) != 0:
            self.rectangles.pop()
        self.update()

    

class WindowClass(PyQt5.QtWidgets.QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Button_dir.clicked.connect(self.img_dir_btn_click)
        self.Button_save.clicked.connect(self.save_btn_click)
        self.Button_load.clicked.connect(self.load_btn_click)
        self.List_img.currentItemChanged.connect(self.img_name_Change)
        
        
        self.Label_screen.setCursor(Qt.CrossCursor)
        self.Label_box = BoxLabel(self)
        self.Label_box.setGeometry(QRect(20, 10, 1024, 768))
        self.Label_box.setCursor(Qt.CrossCursor)

        
        self.image_folder = None
        self.box_object = "character"

        
        self.img = None        
        self.rectangles = None

        self.save_state = "first"
        self.save_info = None

        self.previous_row = -1
        self.json_name = "annotations.json"        

    def keyPressEvent(self, e):
        def isPrintable(key):
            printable = [
                Qt.Key_0, Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4,
                Qt.Key_5,Qt.Key_6,Qt.Key_7,Qt.Key_8,Qt.Key_9,
                Qt.Key_Q, Qt.Key_W,
                Qt.Key_D, Qt.Key_S
            ]

            if key in printable:
                return True
            else:
                return False

        control = False

        if not control and isPrintable(e.key()):
            if self.image_folder != None :
                if e.text() == 'W' or e.text() == 'w' :                    
                    if(self.List_img.currentRow()+1 != self.List_img.count()):
                        self.List_img.setCurrentRow(self.List_img.currentRow()+1)                   

                elif e.text() == 'Q' or e.text() == 'q' :
                    if(self.List_img.currentRow()-1 != -1):
                        self.List_img.setCurrentRow(self.List_img.currentRow()-1)

                elif e.text() == '1' or e.text() == '2' or e.text() == '3' :
                    self.box_object = int(e.text())
                    self.Label_object.setText(object_dict[self.box_object])
                    self.Label_box.obj = self.box_object

                elif e.text() == 'd' or e.text() =='D':
                    self.Label_box.delete_box()
                elif e.text() == 's' or e.text() =='S':
                    self.save_btn_click()
                

    def img_dir_btn_click(self):
        
        tmp = PyQt5.QtWidgets.QFileDialog.getExistingDirectory(self, '이미지 폴더 선택')
        if tmp != "" :
            self.image_folder = tmp
            self.List_img.clear()
            for img_name in os.listdir(self.image_folder) :
                if img_name[-3:] == "jpg" or img_name[-4:] == "jpeg" or img_name[-3:] == "png" :
                    self.List_img.addItem(img_name)

            
            self.save_info = [None] * self.List_img.count()
            self.Button_load.setEnabled(True)
        

    
    def img_name_Change(self):
        if self.List_img.currentItem() != None:
            selected_image = self.image_folder +'/'+ self.List_img.currentItem().text()
            self.img = imdecode(np.fromfile(selected_image,np.uint8), IMREAD_COLOR)
            qimg = PyQt5.QtGui.QPixmap()
            qimg.load(selected_image)            
            self.Label_screen.setPixmap(qimg)


            

            self.update_info()
            self.Label_box.load_rectangles(self.save_info[self.List_img.currentRow()])

            self.previous_row = self.List_img.currentRow()
            self.Label_box.update()

    def update_info(self):
        if self.List_img.currentRow() != -1 and self.previous_row != -1:
            self.save_info[self.previous_row] = self.Label_box.save_rectangle(self.img, self.List_img.item(self.previous_row).text(), self.previous_row)
            print(self.save_info)
            #self.save_info[self.List_img.currentRow()] = self.Label_box.save_rectangle(self.img, self.List_img.currentItem().text(), self.List_img.currentRow())



    def save_btn_click(self):
        self.img_name_Change()
        
        
        coco_form_image_list = list()
        coco_form_anno_list = list()
        print(self.save_info)
        for save_info in self.save_info:
            if save_info != None :                
                if len(save_info) != 1 :
                    ann = save_info[1:]
                    img = save_info[0]
                    coco_form_anno_list.extend(ann)
                    coco_form_image_list.append(img)
        coco_form_image_list = np.array(coco_form_image_list).reshape(-1).tolist()
        coco_form_anno_list = np.array(coco_form_anno_list).reshape(-1).tolist()
        coco_form_dict = {
                         "info":{
                                "num of images" : self.List_img.count(),
                                "num of objects" : len(coco_form_anno_list)
                                },
                         "images":coco_form_image_list,
                         "annotations":coco_form_anno_list,
                         "categories": categories
                        }
                         
        
        with open(self.image_folder+'_'+self.json_name, 'w') as outfile:
            json.dump(coco_form_dict, outfile, indent=4)
        
        now = datetime.datetime.now()
        self.Label_message.setText(str(now).split('.')[0])
    def load_btn_click(self):
        tmp = PyQt5.QtWidgets.QFileDialog.getOpenFileName(self, "JSON 선택", filter = "JSON (*.json)")[0]
        max_ann_id = 1
        if len(tmp) != 0 :
            with open(tmp, "r") as saved_json_dir:

                loaded_json = json.load(saved_json_dir)

            # if self.save_info == None:
            #     self.save_info = [None] * loaded_json["info"]["num of images"]
            
            for img in loaded_json["images"]:
                
                #self.save_info[img["id"]] = [img,[]]
                self.save_info[img["id"]] = [img]

            bbox = list()
            for anno in loaded_json["annotations"] :
                #self.save_info[anno["id"]][1].append(anno)
                self.save_info[anno["image_id"]].append(anno)
                if max_ann_id < anno["id"] :
                    max_ann_id = anno["id"]
            self.Label_box.load_rectangles(self.save_info[self.List_img.currentRow()])
            self.Label_box.update()
            if self.Label_box.ann_ids < max_ann_id+1:
                self.Label_box.ann_ids = max_ann_id+1
        
    

        
if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    myWindow = WindowClass()
    
    myWindow.show()
    app.exec_()
