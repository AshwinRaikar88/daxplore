import os
import shutil
import subprocess
import cv2

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog

from screens.properties import Properties

class ShelfScreen3(QMainWindow):
    def getWidget(self, widget):
        self.widget = widget

    def __init__(self):
        super(ShelfScreen3, self).__init__()

        self.dragPos = QtCore.QPoint()
        self.isMax = False

        loadUi("gui/shelf_3.ui", self)

        if not os.path.exists(f"archive"):
            os.mkdir("archive")

        self.widget = None

        self.path = os.getcwd().replace('\\', '/')
        self.labels = {}
        self.file_list = [""]
        self.index = 0
        self.kb_active = False

        self.shelf.setIcon(QtGui.QIcon('gui/icons/ghost-solid.svg'))
        self.shelf_2.setIcon(QtGui.QIcon('gui/icons/hat-wizard-solid.svg'))
        self.shelf_3.setIcon(QtGui.QIcon('gui/icons/dungeon-solid.svg'))
        self.load_labels.setIcon(QtGui.QIcon('gui/icons/file-solid.svg'))
        self.label_file.setIcon(QtGui.QIcon('gui/icons/open.svg'))
        self.archive_labels.setIcon(QtGui.QIcon('gui/icons/box-archive-solid.svg'))
        self.keyboard_active.setIcon(QtGui.QIcon('gui/icons/keyboard-solid.svg'))
        self.goto_button.setIcon(QtGui.QIcon('gui/icons/goto.svg'))

        self.close_btn.setIcon(QtGui.QIcon('gui/icons/x-mark.svg'))
        self.maximize_btn.setIcon(QtGui.QIcon('gui/icons/maximize.svg'))
        self.minimize_btn.setIcon(QtGui.QIcon('gui/icons/minimize.svg'))

        self.root_dir.setText(self.path)

        # self.treeView.doubleClicked.connect(self.open_file)
        self.close_btn.clicked.connect(self.app_window_controls)
        self.maximize_btn.clicked.connect(self.app_window_controls)
        self.minimize_btn.clicked.connect(self.app_window_controls)

        self.shelf.clicked.connect(self.gotoShelf1)
        self.shelf_2.clicked.connect(self.gotoShelf2)

        self.load_labels.clicked.connect(self.loadLabels)
        self.archive_labels.clicked.connect(self.archive_file)
        self.keyboard_active.clicked.connect(self.activate_keyboard)
        self.goto_button.clicked.connect(self.goto_index)
        self.label_file.clicked.connect(self.open_label)

        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)

        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.treeView.clicked.connect(self.select_item)
        self.treeView.doubleClicked.connect(self.open_file)
        self.populate(self.path)

        self.exp_back.clicked.connect(self.goBack)

    def activate_keyboard(self):
        self.keyboard_active.setStyleSheet("background-color: rgb(0, 255, 0); border-radius: 10px;")

    def deactivate_keyboard(self):
        self.keyboard_active.setStyleSheet("background-color: rgb(222, 222, 222); border-radius: 10px;")

    def open_label(self):
        dst = self.path + f"/{self.file_list[self.index][:-4]}.txt"
        if os.path.exists(dst):
            subprocess.Popen(rf"notepad.exe {dst}")
        else:
            self.show_popup("Open Labels", "Label file does not exist", "warning")

    def goto_index(self):
        text, ok = QInputDialog.getText(self, 'Go to Index', 'Enter file index')

        if ok:
            if int(text) > len(self.file_list):
                self.show_popup("Warning", "Invalid index", "warning")
            elif int(text) <= 0:
                self.show_popup("Warning", "Invalid index", "warning")
            else:
                self.index = int(text) - 1
                self.display_labels(self.path + "/" + self.file_list[self.index])

    def loadLabels(self):
        text, ok = QInputDialog.getText(self, 'Load Labels', 'Label filepath')
        if ok:
            colors = [(4, 67, 137), (252, 255, 75), (255, 173, 5), (124, 61, 196), (255, 60, 5)]
            if os.path.exists(text) and text[-4:] == '.txt':
                file = open(text, 'r')
                count = 0
                for line in file.readlines():
                    line = line.replace("\n", "")
                    self.labels.update({count: (line, colors[count])})
                    count += 1
                self.load_labels.setStyleSheet("background-color: rgb(170, 255, 0); border-radius: 10px;")
                self.show_popup('Load Labels', 'Labels loaded', 'info')

            else:
                self.show_popup('Load Labels', 'Label file does not exist', 'warning')

    def select_item(self):
        self.kb_active = False
        self.deactivate_keyboard()

        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        self.title_count.setText(f"     {self.model.fileName(index)}")

        if file_path[-4:] == ".jpg" or file_path[-4:] == ".png":
            self.display_labels(file_path)
        elif os.path.exists(file_path) and os.path.exists(file_path[-4:]+".txt"):
            self.display_labels(file_path)

    def keyPressEvent(self, event):
        self.kb_active = True
        self.activate_keyboard()
        if event.key() == QtCore.Qt.Key_B:
            self.index -= 1

            if self.index < 0:
                self.index = 0

            dst = self.path + f"/{self.file_list[self.index]}"
            self.display_labels(dst)
            self.root_dir.setText(dst)

        elif event.key() == QtCore.Qt.Key_N:
            self.index += 1

            if self.index >= len(self.file_list):
                self.index -= 1

            dst = self.path + f"/{self.file_list[self.index]}"
            self.display_labels(dst)
            self.root_dir.setText(dst)

    def resizeEvent(self, resizeEvent):
        self.widget_1.resize(self.width(), 120)
        self.widget_2.resize(self.width(), self.height())
        self.root_dir.resize(self.width()-130, 50)
        self.action_window.resize(self.width() - 430, self.height() - 230)
        self.treeView.resize(350, self.height() - 250)
        self.tree_background.resize(350, self.height() - 230)
        self.picBox.resize(self.width() - 450, self.height() - 270)
        self.title_bar.resize(self.width(), 40)
        self.close_btn.move(self.width() - 30, 10)
        self.maximize_btn.move(self.width() - 60, 10)
        self.minimize_btn.move(self.width() - 90, 10)

        self.keyboard_active.move(self.width() - 500, self.height() - 360)
        self.goto_button.move(20, self.height() - 360)
        self.title_count.resize(self.width() - 450, 40)
        self.title_count.move(10, self.height() - 300)

    def context_menu(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction("Open")
        rename = menu.addAction("Rename")
        properties = menu.addAction("Properties")
        menu.addSeparator()
        archive = menu.addAction("Archive")
        delete = menu.addAction("Delete")

        open.setIcon(QtGui.QIcon('gui/icons/open.svg'))
        rename.setIcon(QtGui.QIcon('gui/icons/rename.svg'))
        properties.setIcon(QtGui.QIcon('gui/icons/info-solid.svg'))
        archive.setIcon(QtGui.QIcon('gui/icons/box-archive-solid.svg'))
        delete.setIcon(QtGui.QIcon('gui/icons/trash-solid.svg'))

        open.triggered.connect(self.open_file)
        rename.triggered.connect(self.rename_file)
        archive.triggered.connect(self.archive_file)
        delete.triggered.connect(self.delete_file)
        properties.triggered.connect(self.show_properties)

        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def open_file(self):
        self.kb_active = False
        self.deactivate_keyboard()
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        file_name = self.model.fileName(index)
        self.title_count.setText(f"     {file_name}")

        if os.path.isdir(file_path):
            self.path = file_path
            self.root_dir.setText(self.path)
            self.populate(file_path)
            self.parse_files()

        elif file_path[-4:] == ".jpg" or file_path[-4:] == ".png":
            self.display_labels(file_path)

        # elif file_path[-4:] == ".txt":
        #     diag = Properties(file_name, 't')

        elif os.path.exists(file_path) and os.path.exists(file_path[-4:]+".txt"):
            self.display_labels(file_path)

        print(f'clicked: {file_path}')

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

    def archive_file(self):
        if self.kb_active:
            file_path = self.root_dir.text()
        else:
            index = self.treeView.currentIndex()
            file_path = self.model.filePath(index)

        if os.path.isdir(file_path):
            dst = f"archive/{os.path.basename(file_path)}"
            shutil.move(file_path, dst)
        else:
            dst = os.path.abspath(file_path + f"/../")
            dst = f"archive/{os.path.basename(dst)}"
            if not os.path.exists(dst):
                os.mkdir(dst)

            shutil.move(file_path, dst)
            if self.kb_active:
                self.file_list.pop(self.index)
                self.index -= 1

            # Move labels if found
            if os.path.exists(file_path[:-4]+".txt"):
                shutil.move(file_path[:-4]+".txt", dst)

            image_qt = QImage("gui/images/archived-rubber-stamp.jpg")

            # To scale image for example and keep its Aspect Ratio
            image_qt = image_qt.scaled(self.picBox.width(), self.picBox.height(),
                                       aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                       transformMode=QtCore.Qt.SmoothTransformation)
            self.picBox.setPixmap(QPixmap.fromImage(image_qt))

        print(f'Archived: {dst}')

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

    def show_properties(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        file_name = os.path.basename(file_path)

        if os.path.isdir(file_path):
            diag = Properties(file_name, file_path, 'd')

        elif file_path[-4:] == ".jpg" or file_path[-4:] == ".png":
            diag = Properties(file_name, file_path, 'e')

        elif file_path[-4:] == ".txt":
            diag = Properties(file_name, file_path, 't')
        else:
            diag = Properties(file_name, file_path, 'f')

        diag.setModal(False)
        diag.exec()

    def display_labels(self, filepath):
        label_error = ""
        lbl_path = os.path.abspath(filepath + "/../../../") + "/labels/" + os.path.basename(os.path.abspath(filepath + "/../")) + "/" + f"{os.path.basename(filepath)[:-4]}.txt"
        if not os.path.exists(lbl_path):
            lbl_path = filepath[:-4]+".txt"

        if self.kb_active:
            self.title_count.setText(f"     Count: {self.index + 1}/{len(self.file_list)} {self.file_list[self.index]}")

        if os.path.exists(lbl_path):
            label_file = open(lbl_path, 'r')
            lines = label_file.readlines()
            label_file.close()

            img = cv2.imread(filepath)
            dh, dw, _ = img.shape

            scale = 1
            # if 640 < dw < 1080:
            #     scale = 1
            if 1080 < dw < 2048:
                scale = 2
            elif 2048 < dw:
                scale = 3

            for line in lines:
                # Split string to float
                class_name, nx, ny, nw, nh = map(str, line.split(' '))
                nx, ny, nw, nh = map(float, [nx, ny, nw, nh])

                l = int((nx - nw / 2) * dw)
                r = int((nx + nw / 2) * dw)
                t = int((ny - nh / 2) * dh)
                b = int((ny + nh / 2) * dh)

                if l < 0:
                    l = 0
                    label_error += "L "
                if r > dw - 1:
                    r = dw - 1
                    label_error += "R "
                if t < 0:
                    t = 0
                    label_error += "T "
                if b > dh - 1:
                    b = dh - 1
                    label_error += "B "

                if len(self.labels) > 0:
                    if len(class_name) > 3:
                        for key, value in self.labels.items():
                            if class_name == value[0]:
                                cv2.putText(img, f"{self.labels[key][0]}", (l + 5, t + 20*scale),
                                            cv2.FONT_HERSHEY_SIMPLEX, scale, self.labels[key][1], scale+2, cv2.LINE_AA, False)
                                if label_error != "":
                                    cv2.putText(img, f"label error {label_error}", (l + 5, t + 40 * scale),
                                                cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 0, 255), scale + 2,
                                                cv2.LINE_AA, False)

                                cv2.rectangle(img, (l, t), (r, b), self.labels[key][1], 3)
                                break
                            else:
                                cv2.putText(img, class_name, (l+5, t+20*scale), cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 0, 255), scale+2,
                                        cv2.LINE_AA, False)
                                cv2.rectangle(img, (l, t), (r, b), (0, 255, 0), 3)
                    else:
                        try:
                            cv2.putText(img, self.labels[int(class_name)][0], (l+5, t+20), cv2.FONT_HERSHEY_SIMPLEX, 1, self.labels[int(class_name)][1], 3,  cv2.LINE_AA, False)
                            cv2.rectangle(img, (l, t), (r, b), self.labels[int(class_name)][1], 3)
                        except:
                            "Index out of range exception"
                            cv2.putText(img, class_name, (l + 5, t + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                                        3, cv2.LINE_AA, False)
                            cv2.rectangle(img, (l, t), (r, b), (0, 255, 0), 3)
                else:
                    cv2.rectangle(img, (l, t), (r, b), (0, 255, 0), 3)

            cv2.imwrite("_temp.jpg", img)
            image_qt = QImage("_temp.jpg")
        else:
            image_qt = QImage(filepath)

        image_qt = image_qt.scaled(self.picBox.width(), self.picBox.height(), aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                             transformMode=QtCore.Qt.SmoothTransformation)  # To scale image for example and keep its Aspect Ratio
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
        self.root_dir.setText(self.path)
        self.populate(self.path)

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

    def parse_files(self):
        self.index = 0
        for dir_obj in os.walk(self.path):
            # self.path = dir_obj[0]
            # dirs = dir_obj[1]
            self.file_list = [file for file in dir_obj[2] if not file.endswith(('.txt', '.tar'))]
            # self.file_list = dir_obj[2]

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self.title_bar.underMouse():
            self.widget.move(self.widget.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def app_window_controls(self):
        if self.maximize_btn.underMouse():
            if self.isMax:
                self.widget.showNormal()
                self.isMax = False
                self.maximize_btn.setIcon(QtGui.QIcon('gui/icons/maximize.svg'))
            else:
                self.widget.showFullScreen()
                self.isMax = True
                self.maximize_btn.setIcon(QtGui.QIcon('gui/icons/normal.svg'))
        elif self.minimize_btn.underMouse():
            self.widget.showMinimized()
        elif self.close_btn.underMouse():
            self.widget.close()
