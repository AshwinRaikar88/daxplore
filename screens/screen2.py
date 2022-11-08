import math
import os
import shutil
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QMessageBox, QInputDialog, QSizePolicy

def splitter(src, dst, ext="txt"):
    _, _, files = next(os.walk(src))
    files = [fi for fi in files if fi.endswith(f".{ext}")]
    file_count = len(files)

    print(file_count)
    ratio = math.floor(file_count*0.7)
    count = 0
    for filename in files:
        if count < ratio:
            shutil.copy(src+f"/{filename}", dst+f"/train/{filename}")
        else:
            shutil.copy(src+f"/{filename}", dst+f"/val/{filename}")

        count += 1

class ShelfScreen2(QMainWindow):
    def __init__(self):
        super(ShelfScreen2, self).__init__()
        loadUi("gui/shelf_2.ui", self)

        self.widget = None

        self.path = os.getcwd().replace('\\', '/')
        self.root_dir.setText(self.path)

        self.shelf.setIcon(QtGui.QIcon('gui/icons/ghost-solid.png'))
        self.shelf_2.setIcon(QtGui.QIcon('gui/icons/hat-wizard-solid.svg'))
        self.shelf_3.setIcon(QtGui.QIcon('gui/icons/dungeon-solid.svg'))

        self.shelf.clicked.connect(self.gotoShelf1)
        self.shelf_3.clicked.connect(self.gotoShelf3)

        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.clicked.connect(self.select_item)
        # self.treeView.doubleClicked.connect(self.open_file)

        self.checkBox_txt.setChecked(True)
        self.checkBox_txt.clicked.connect(self.toggleChkBx2)
        self.checkBox_img.clicked.connect(self.toggleChkBx1)
        self.exp_back.clicked.connect(self.goBack)
        self.startB.clicked.connect(self.startSplit)

        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)
        self.treeView.doubleClicked.connect(self.open_file)

        self.populate(self.path)

    def select_item(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        if os.path.isdir(file_path):
            self.src_text_box.setText(file_path)

    def toggleChkBx1(self):
        self.checkBox_txt.setChecked(False)
        self.checkBox_img.setChecked(True)

    def toggleChkBx2(self):
        self.checkBox_img.setChecked(False)
        self.checkBox_txt.setChecked(True)

    def startSplit(self):
        src = self.src_text_box.text()
        dest = self.dest_text_box.text()

        if os.path.exists(src):
            if os.path.exists(dest):
                self.show_popup('Warning', 'Destination Dir already exists', 'warning')
            else:
                os.mkdir(dest)
                os.mkdir(dest+"/train")
                os.mkdir(dest+"/val")

                if self.checkBox_txt.isChecked():
                    "Starting splitting for txt files"
                    splitter(src, dest, 'txt')
                    self.show_popup('Splitting ', 'Splitting Completed', 'info')
                elif self.checkBox_img.isChecked():
                    "Starting splitting for img files"
                    splitter(src, dest, 'jpg')
                    self.show_popup('Splitting', 'Splitting Completed', 'info')

        else:
            self.show_popup('Warning', 'Source Dir not found', 'warning')

    def context_menu(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction("Open")
        rename = menu.addAction("Rename")
        menu.addSeparator()
        delete = menu.addAction("Delete")

        open.setIcon(QtGui.QIcon('gui/icons/open.svg'))
        rename.setIcon(QtGui.QIcon('gui/icons/rename.svg'))
        delete.setIcon(QtGui.QIcon('gui/icons/trash-solid.svg'))

        open.triggered.connect(self.open_file)
        rename.triggered.connect(self.rename_file)
        delete.triggered.connect(self.delete_file)

        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def open_file(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)

        if os.path.isdir(file_path):
            self.path = file_path
            self.root_dir.setText(self.path)
            self.src_text_box.setText(self.path)
            self.populate(file_path)

    def rename_file(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)

        if os.path.isdir(file_path):
            text, ok = QInputDialog.getText(self, 'Rename folder', 'Enter new folder name')

            if ok:
                dst = os.path.abspath(file_path+f"/../{text}")
                try:
                    os.rename(file_path, dst)
                except Exception as ex:
                    self.show_popup("Warning", ex, 'warning')
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
        self.src_text_box.setText(self.path)

    def populate(self, path):
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(path))
        self.treeView.setSortingEnabled(True)

    def resizeEvent(self, resizeEvent):
        self.widget_1.resize(self.width(), 120)
        self.widget_2.resize(self.width(), self.height())
        self.root_dir.resize(self.width()-130, 50)
        self.action_window.resize(self.width() - 430, self.height() - 250)
        self.treeView.resize(350, self.height() - 250)

    def getWidget(self, widget):
        self.widget = widget

    def gotoShelf1(self):
        self.widget.setCurrentIndex(0)

    def gotoShelf3(self):
        self.widget.setCurrentIndex(2)