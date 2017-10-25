# -*- coding: utf-8 -*-

# import numpy
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import TextLocalize as tl
import ocr_trans as ot
from PIL import Image,ImageFont,ImageDraw
#

import sys
# from PyQt4 import QtCore, QtGui
from ui import Ui_UI

header = ['x', 'y', 'w', 'h', 'original text', 'translated text']

def print_change(index, index2):
    print("changed", index)


def cv2QImage(img):
    out = img.copy()
    height, width, byteValue = img.shape
    byteValue = byteValue * width

    cv2.cvtColor(img, cv2.COLOR_BGR2RGB, out)

    mQImage = QImage(out, width, height, byteValue, QImage.Format_RGB888)
    return mQImage

class MyTableModel(QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist.copy()
        self.header = header.copy()
        self.dataChanged.connect(print_change)

    def rowCount(self, parent):
        return len(self.mylist)
    def columnCount(self, parent):
        return len(self.mylist[0])
    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole and role != Qt.EditRole:
            return None
        return self.mylist[index.row()][index.column()]
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None
    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return None
        elif role != Qt.EditRole:
            return None
        # print(index.row(),index.column(), self.mylist[index.row()][index.column()])
        try:
            self.mylist[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
        except:
            print("Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])
        return True


class MyDialog(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_UI()
        self.ui.setupUi(self)
        self.ui.LoadImg.clicked.connect(lambda: self.loadImage())
        self.ui.AutoDetect.clicked.connect(lambda: self.autoDetect())
        self.ui.Translate.clicked.connect(lambda: self.translate())
        self.ui.Export.clicked.connect(lambda: self.export())

    def loadImage(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '.', "Image files (*.jpg *.gif *.png)")
        self.cvImage = cv2.imread(fname)
        self.ui.updateImage(cv2QImage(self.cvImage))

    def autoDetect(self):
        margin = 3
        self.coord_list, autodetect_image = tl.localizeText(self.cvImage)
        for item in self.coord_list:
            roi = self.cvImage[item[1] - margin:item[1]+item[3] + margin, item[0]- margin:item[0]+item[2] + margin].copy()
            text = ''
            try:
                text = ot.ocr(roi)
                # words = text.split(' ')
                # words = text.replace(' ', ';')
                # corrected = ot.text_correction(words)
                # corrected =  ' '.join(corrected)

                # corrected = ' '.join([ot.local_correction(word) for word in words])
                print('OCR text:\n--{}--'.format(text))
            except:
                print("Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])
            # item[4] = textX
            item.append(text)
            item.append('')

        self.ui.updateImage(cv2QImage(autodetect_image))
        table_model = MyTableModel(self, self.coord_list, header)
        self.ui.updateTable(table_model)
        self.ui.tableView.selectionModel().selectionChanged.connect(self.selChanged)

    def  selChanged(self, selected, deselected):
        # print('changed', selected, deselected)
        indexes = self.ui.tableView.selectionModel().selectedIndexes()
        index = indexes[0]
        print(index.row(),index.column())

    def translate(self):
        # margin = 2
        for item in self.coord_list:
            # roi = self.cvImage[item[1] - margin:item[1]+item[3] + margin, item[0]- margin:item[0]+item[2] + margin].copy()
            # print(roi.shape)
            try:
                translation = ot.trans(item[4])
                print('translation result:', translation)
                item[5] = translation
            except:
                print("Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])
        table_model = MyTableModel(self, self.coord_list, header)
        self.ui.updateTable(table_model)

    def export(self):
        boxes = []
        translated_text = []
        for item in self.coord_list:
            if item[2] == 0 or item[3] == 0:
                continue
            if len(item[4]) == 0:
                continue
            boxes.append(item[0:4])
            translated_text.append(item[5])

        background = tl.extractBackgnd(boxes, self.cvImage)
        # font = cv2.FONT_HERSHEY_SIMPLEX

        cv2.cvtColor(background, cv2.COLOR_BGR2RGB, background)
        img = Image.fromarray(background)
        draw = ImageDraw.Draw(img)
        for box, text in zip(boxes, translated_text):
            try:
                fontim = ImageFont.truetype('simhei.ttf', box[3])
                draw.text((box[0], box[1]), text, font=fontim, fill=(0,0,0,255))
            except:
                print("Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])
            # cv2.putText(background, text, (box[0], box[1] + box[3]), font, 0.5, (200, 255, 155), 1, cv2.LINE_AA)
        cv2.imwrite('background.jpg', background)
        img.save('translated.jpg', "JPEG")
        # img.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyDialog()
    myapp.show()
    sys.exit(app.exec_())

