import os
import shutil
import cv2

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QMessageBox, QInputDialog, QSizePolicy


class ShelfScreen3(QMainWindow):
    def getWidget(self, widget):
        self.widget = widget

    def __init__(self):
        super(ShelfScreen3, self).__init__()
        loadUi("gui/shelf_3.ui", self)

        self.widget = None

        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)

        self.path = os.getcwd().replace('\\', '/')
        self.root_dir.setText(self.path)

        icon1 = QtGui.QIcon('gui/icons/ghost-solid.png')
        self.shelf.setIcon(icon1)

        icon2 = QtGui.QIcon('gui/icons/hat-wizard-solid.svg')
        self.shelf_2.setIcon(icon2)

        icon3 = QtGui.QIcon('gui/icons/dungeon-solid.svg')
        self.shelf_3.setIcon(icon3)

        self.shelf.clicked.connect(self.gotoShelf1)
        self.shelf_2.clicked.connect(self.gotoShelf2)

        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.treeView.clicked.connect(self.select_item)
        self.treeView.doubleClicked.connect(self.open_file)
        self.populate(self.path)


        self.exp_back.clicked.connect(self.goBack)

    def select_item(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)

        if file_path[-4:] == ".jpg" or file_path[-4:] == ".png":
            self.display_labels(file_path)
        elif os.path.exists(file_path) and os.path.exists(file_path[-4:]+".txt"):
            self.display_labels(file_path)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_B:
            self.goBack()
            print(" Pressed B")

        elif event.key() == QtCore.Qt.Key_N:
            print(" Pressed N")


    def resizeEvent(self, resizeEvent):
        self.widget_1.resize(self.width(), 120)
        self.widget_2.resize(self.width(), self.height())
        self.root_dir.resize(self.width()-130, 50)
        self.action_window.resize(self.width() - 430, self.height() - 250)
        self.picBox.resize(self.width() - 450, self.height() - 270)
        self.treeView.resize(350, self.height() - 250)

    def context_menu(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction("Open")
        rename = menu.addAction("Rename")
        delete = menu.addAction("Delete")

        open.triggered.connect(self.open_file)
        rename.triggered.connect(self.rename_file)
        delete.triggered.connect(self.delete_file)

        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def open_file(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        file_name = os.path.basename(file_path)

        if os.path.isdir(file_path):
            self.path = file_path
            self.root_dir.setText(self.path)
            self.populate(file_path)
            diag = Properties(file_name, 'd')

        elif file_path[-4:] == ".jpg" or file_path[-4:] == ".png":
            self.display_labels(file_path)
            diag = Properties(file_name, 'e')

        elif file_path[-4:] == ".txt":
            diag = Properties(file_name, 't')

        elif os.path.exists(file_path) and os.path.exists(file_path[-4:]+".txt"):
            self.display_labels(file_path)

        print(f'clicked: {file_path} {file_path[-4:]}')
        diag.setModal(True)
        diag.exec()


    def rename_file(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)

        if os.path.isdir(file_path):
            text, ok = QInputDialog.getText(self, 'Rename folder', 'Enter new folder name')

            if ok:
                dst = os.path.abspath(file_path+f"/../{text}")
                os.rename(file_path, dst)
                print(f'rename: {dst}')
        else:
            print("Not a dir")

    def delete_file(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)

        if os.path.isdir(file_path):
            qD = QMessageBox()
            qD.setWindowTitle("Delete File")
            qD.setText("Are you sure you want to delete this file ?")
            qD.setIcon(QMessageBox.Warning)
            qD.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            qD.setDefaultButton(QMessageBox.No)

            ok = qD.exec_()

            if ok == 16384:
                shutil.rmtree(file_path, True)
                # dst = self.path + f"/{text}"
                # os.rename(file_path, dst)
                print(f'deleted: {ok}')
        else:
            print("Not a dir")

    def display_labels(self, filepath):

        if os.path.exists(filepath[:-4]+".txt"):

            label_file = open(filepath[:-4]+".txt", 'r')
            lines = label_file.readlines()
            label_file.close()

            img = cv2.imread(filepath)
            dh, dw, _ = img.shape

            for line in lines:
                print(line)
                # Split string to float
                class_name, nx, ny, nw, nh = map(float, line.split(' '))

                l = int((nx - nw / 2) * dw)
                r = int((nx + nw / 2) * dw)
                t = int((ny - nh / 2) * dh)
                b = int((ny + nh / 2) * dh)

                if l < 0:
                    l = 0
                if r > dw - 1:
                    r = dw - 1
                if t < 0:
                    t = 0
                if b > dh - 1:
                    b = dh - 1

                cv2.rectangle(img, (l, t), (r, b), (0, 255, 0), 3)

            cv2.imwrite("_temp.jpg", img)
            image_qt = QImage("_temp.jpg")
        else:
            image_qt = QImage(filepath)

        image_qt = image_qt.scaled(self.picBox.width(), self.picBox.height(), aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                             transformMode=QtCore.Qt.SmoothTransformation)  # To scale image for example and keep its Aspect Ration
        self.picBox.setPixmap(QPixmap.fromImage(image_qt))

    def show_popup(self, title, info, type):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(info)
        msg.setDefaultButton(QMessageBox.Ok)
        if type == "warning":
            # Question, Information, Warning
            msg.setIcon(QMessageBox.Warning)
        elif type == "info":
            msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def goBack(self):
        self.path = os.path.abspath(self.path + "/../").replace('\\', '/')
        self.populate(self.path)
        self.root_dir.setText(self.path)
        print(self.path)

    def populate(self, path):
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(path))
        self.treeView.setSortingEnabled(True)

    def gotoShelf1(self):
        self.widget.setCurrentIndex(0)

    def gotoShelf2(self):
         self.widget.setCurrentIndex(1)

class Properties(QDialog):
    def __init__(self, fileName="Default", dir="d"):
        super(QDialog, self).__init__()
        loadUi("gui/properties.ui", self)

        self.filename.setText(fileName)

        if dir == "d":
            icon = QtGui.QIcon('../gui/icons/ghost-solid.png')
            self.shelf.setIcon(icon)
        elif dir == "e":
            icon = QtGui.QIcon('../gui/icons/hat-wizard-solid.svg')
            self.shelf.setIcon(icon)
        elif dir == "t":
            icon = QtGui.QIcon('../gui/icons/dungeon-solid.svg')
            self.shelf.setIcon(icon)