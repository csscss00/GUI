# coding=utf-8
import sys
from PyQt5.QtWidgets import  QApplication, QWidget, QDialog, QFileDialog
from PyQt5.QtCore import  pyqtSlot
from Widget import Ui_Widget
import configparser
from PyQt5.QtGui import QPixmap, QImage
import os, cv2
import numpy as np

#
##

def string2intlist(str_in):
   ##
   # 1: remove ' ', '[', and ']'
   # 2: split into string list
   # 3: convert into int list
   temp = str_in.replace(' ', '').replace(' ', '').replace('[', '').replace(']', '').split(',')
   # temp_int_list = [float(x) for x in temp]
   temp_int_list = []
   for x in temp:
      if x is not '':
         temp_int_list.append(float(x))
   return temp_int_list

class QmyWidget(QWidget):
   def __init__(self, parent=None, Img_path=None, XML_path=None):
      super().__init__(parent)   #调用父类构造函数，创建窗体
      self.ui=Ui_Widget()        #创建UI对象
      self.ui.setupUi(self)      #构造UI界面
      # Widget.setFixedSize(766, 750)

      self.Img_path = Img_path
      self.XML_path = XML_path
      # self.ui.groupBox_Train.setFixedSize(800, 100)
      self.ui.radioButtonSave.setChecked(False)
      self.ui.radioButtonSave.toggled.connect(self.btnSaveorNot)

   def btnSaveorNot(self):#预测结果是否保存在本地
      radiobutton = self.sender()
      if radiobutton.isChecked() == True:
         self.is_log = 1
      else:
         self.is_log = 0

   @pyqtSlot()
   def on_btnOPenini_clicked(self):
      dir = 'G:\DefectDetectorMain\config'
      fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                              "选取文件",
                                                              directory=dir,
                                                              filter="(*.ini)")  # 设置文件扩展名过滤,用双分号间隔

      if fileName_choose == "":
         print("\n取消选择")
         return
      print("\n你选择的文件为:")
      print(fileName_choose)

      conf = configparser.ConfigParser()
      conf.read(fileName_choose, encoding="utf-8")
      sections = conf.sections()
      section1 = conf.items('common')
      PIXEL_MEAN = conf.get('common', 'PIXEL_MEAN')
      PIXEL_MEAN = string2intlist(PIXEL_MEAN)

      self.ui.editR.setText('%.2f' % PIXEL_MEAN[0])
      self.ui.editG.setText('%.2f' % PIXEL_MEAN[1])
      self.ui.editB.setText('%.2f' % PIXEL_MEAN[2])

   @pyqtSlot()
   def on_btnReview_clicked(self):  ##"预览"按钮
      ImgR = float(self.ui.editR.text())
      ImgG = float(self.ui.editG.text())
      ImgB = float(self.ui.editB.text())
      Img_review = np.zeros((200,200,3))
      Img_review[:, :, 0] = ImgB
      Img_review[:, :, 1] = ImgG
      Img_review[:, :, 2] = ImgR

      Img_review = Img_review.astype("uint8")
      width, height = Img_review.shape[:2]
      qImg = QImage(Img_review.data, width, height, height*3, QImage.Format_RGB888).rgbSwapped()
      self.ui.labelReview.setPixmap(QPixmap.fromImage(qImg))

      # cv2.imwrite('review.jpg', Img_review)
      # jpg = QPixmap('review.jpg')      # jpg = QPixmap('timg (1).jpg')
      # self.ui.labelReview.setPixmap(jpg)
      self.ui.labelReview.setScaledContents(True)

   ##  ==========保存按钮连接的槽函数===============
   @pyqtSlot()
   def on_btnSave_clicked(self):  ##"保存"按钮
      ImgR = float(self.ui.editR.text())
      ImgG = float(self.ui.editG.text())
      ImgB = float(self.ui.editB.text())
      # for i in range(18):
      #     Def_Name = 'Def_Name'+i
      #     Def_The = 'Def_The'+i
      #     editFect = 'editFect'+i
      #     editThe = 'editThe'+i
      editFects = [
         self.ui.editFect1,
         self.ui.editFect2,
         self.ui.editFect3,
         self.ui.editFect4,
         self.ui.editFect5,
         self.ui.editFect6,
         self.ui.editFect7,
         self.ui.editFect8,
         self.ui.editFect9,
         self.ui.editFect10,
         self.ui.editFect11,
         self.ui.editFect12,
         self.ui.editFect13,
         self.ui.editFect14,
         self.ui.editFect15,
         self.ui.editFect16,
         self.ui.editFect17,
         self.ui.editFect18,
      ]

      editThes = [
         self.ui.editThe1,
         self.ui.editThe2,
         self.ui.editThe3,
         self.ui.editThe4,
         self.ui.editThe5,
         self.ui.editThe6,
         self.ui.editThe7,
         self.ui.editThe8,
         self.ui.editThe9,
         self.ui.editThe10,
         self.ui.editThe11,
         self.ui.editThe12,
         self.ui.editThe13,
         self.ui.editThe14,
         self.ui.editThe15,
         self.ui.editThe16,
         self.ui.editThe17,
         self.ui.editThe18,
      ]

      Def_Names = []
      Def_Thes = []

      for i in range (len(editFects)):
         if editFects[i].text()!='':
            Def_Names.append(editFects[i].text())
            Def_Thes.append(float(editThes[i].text()))

      LABEL_NAMES_str = '['
      LABEL_THRESH_str = '['
      for i in range(len(Def_Names)):
         if i != len(Def_Names)-1:
            LABEL_NAMES_str += '%s,'
            LABEL_THRESH_str += '%f,'
         else:
            LABEL_NAMES_str += '%s]'
            LABEL_THRESH_str += '%f]'

      print(LABEL_NAMES_str, tuple(Def_Names))
      lines_LABEL_NAMES = LABEL_NAMES_str % tuple(Def_Names)
      lines_LABEL_THRESH = LABEL_THRESH_str % tuple(Def_Thes)
      print(lines_LABEL_NAMES)

      #读取界面中输入的参数
      lines_PIX_mean ='[%f,%f,%f]' % (ImgR, ImgG, ImgB)
      # lines_LABEL_NAMES = '[%s,%s,%s,%s,%s,%s]' %(Def_Name1, Def_Name2, Def_Name3, Def_Name4, Def_Name5, Def_Name6)
      # lines_LABEL_THRESH = '[%f,%f,%f,%f,%f,%f]' % (Def_The1, Def_The2, Def_The3, Def_The4, Def_The5, Def_The6)
      lines_MAX_ITERATION= int(self.ui.editMax_iteration.text())
      lines_SAVE_WEIGHTS_INTE = int(self.ui.editSave_inter.text())
      lines_train_images_path = self.ui.editImgpath.text()
      lines_train_XML_path = self.ui.editXMLpath.text()

      print(lines_MAX_ITERATION)

      #生成config.ini文件
      config = configparser.ConfigParser()
      config.add_section("common")
      config.set("common", "base_trained_ckpt_full_path", "./weights/base_trained/resnet_v1_101.ckpt")
      config.set("common", "all_trained_ckpt_path", "./weights/all_trained/")
      config.set("common", "LABEL_NAMES ", lines_LABEL_NAMES)
      config.set("common", "PIXEL_MEAN", lines_PIX_mean)

      config.add_section("prediction")
      config.set("prediction", "src_path", "D:/codes/inferenceSRC/")
      config.set("prediction", "dst_path ", "D:/codes/inferenceDST/")
      config.set("prediction", "image_filter ", ".bmp")
      config.set("prediction", "LABEL_THRESH  ", lines_LABEL_THRESH)
      config.set("prediction", "server_ip ", "127.0.0.1")
      config.set("prediction", "server_port ", "21566")
      config.set("prediction", "is_log ", str(self.is_log))

      config.add_section("train")
      config.set("train", "MAX_ITERATION", str(lines_MAX_ITERATION))
      config.set("train", "SAVE_WEIGHTS_INTE", str(lines_SAVE_WEIGHTS_INTE))
      config.set("train", "train_images_path", lines_train_images_path)
      config.set("train", "train_xmls_path ", lines_train_XML_path)

      saveName = self.ui.editSavename.text()
      config.write(open(saveName, mode='w', encoding='utf-8'))

   @pyqtSlot()
   def on_btnImg_clicked(self):
      if self.Img_path is not None:
         path = self.Img_path
      else:
         path = '.'
      dirpath = QFileDialog.getExistingDirectory(self,
                                                 'choose the images directory', path,
                                                 QFileDialog.ShowDirsOnly
                                                 | QFileDialog.DontResolveSymlinks)

      if dirpath is not None and len(dirpath) > 1:
         self.Img_path = dirpath
         self.ui.editImgpath.setText(self.Img_path)

   @pyqtSlot()
   def on_btnXML_clicked(self):
      if self.XML_path is not None:
         path = self.XML_path
      else:
         path = '.'
      dirpath = QFileDialog.getExistingDirectory(self,
                                                 'choose the XML directory', path,
                                                 QFileDialog.ShowDirsOnly
                                                 | QFileDialog.DontResolveSymlinks)

      if dirpath is not None and len(dirpath) > 1:
         self.XML_path = dirpath
         self.ui.editXMLpath.setText(self.XML_path)

if  __name__ == "__main__":         #用于当前窗体测试
   app = QApplication(sys.argv)     #创建GUI应用程序
   form=QmyWidget()                 #创建窗体
   form.show()
   sys.exit(app.exec_())
