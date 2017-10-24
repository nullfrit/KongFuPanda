# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_UI(object):
    def setupUi(self, UI):
        UI.setObjectName("UI")
        UI.setWindowModality(QtCore.Qt.ApplicationModal)
        UI.resize(1024, 600)
        self.gridLayout_3 = QtWidgets.QGridLayout(UI)
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.graphicsView = QtWidgets.QGraphicsView(UI)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout_2.addWidget(self.graphicsView)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(UI)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.LoadImg = QtWidgets.QPushButton(UI)
        self.LoadImg.setObjectName("LoadImg")
        self.gridLayout_2.addWidget(self.LoadImg, 0, 0, 1, 1)
        self.AutoDetect = QtWidgets.QPushButton(UI)
        self.AutoDetect.setObjectName("AutoDetect")
        self.gridLayout_2.addWidget(self.AutoDetect, 0, 1, 1, 1)
        self.Translate = QtWidgets.QPushButton(UI)
        self.Translate.setObjectName("Translate")
        self.gridLayout_2.addWidget(self.Translate, 1, 0, 1, 1)
        self.Export = QtWidgets.QPushButton(UI)
        self.Export.setObjectName("Export")
        self.gridLayout_2.addWidget(self.Export, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.scene = QtWidgets.QGraphicsScene()

        self.retranslateUi(UI)
        QtCore.QMetaObject.connectSlotsByName(UI)



    def retranslateUi(self, UI):
        _translate = QtCore.QCoreApplication.translate
        UI.setWindowTitle(_translate("UI", "AutoMenuTranslator"))
        self.LoadImg.setText(_translate("UI", "LoadImg"))
        self.AutoDetect.setText(_translate("UI", "AutoDetect"))
        self.Translate.setText(_translate("UI", "Translate"))
        self.Export.setText(_translate("UI", "Export"))

    def updateImage(self, img):
        self.scene.clear()
        pixMap = QtGui.QPixmap.fromImage(img)
        self.scene.addPixmap(pixMap)
        # self.graphicsView.fitInView(QRectF(0, 0, w, h), Qt.KeepAspectRatio)
        self.graphicsView.setScene(self.scene)
        self.scene.update()

    def updateTable(self, table_model):
        self.tableView.setModel(table_model)
        self.tableView.resizeColumnsToContents()
