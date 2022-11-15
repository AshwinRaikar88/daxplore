import math
import os
import shutil
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog

def splitter(src, dst, split):
    _, _, src_files = next(os.walk(src))
    exts = {'labels': '.txt', 'images': ('.jpg', '.png')}
    os.mkdir(dst)

    for key, value in exts.items():
        files = [fi for fi in src_files if fi.endswith(value)]
        file_count = len(files)

        if file_count != 0:
            os.mkdir(dst + f"/{key}")
            os.mkdir(dst + f"/{key}/train")
            os.mkdir(dst + f"/{key}/val")

            ratio = math.floor(file_count * (split / 10))
            count = 0
            tr = 0
            valc = 0
            for filename in files:
                if count < ratio:
                    tr += 1
                    shutil.copy(src + f"/{filename}", dst + f"/{key}/train/{filename}")
                else:
                    valc += 1
                    shutil.copy(src + f"/{filename}", dst + f"/{key}/val/{filename}")

                count += 1
            print(f"Total {value} files = {count}\n-----------------------\nSplit {split*10}:{100-split*10}\nTrain = {tr} Val = {valc}\n")
        else:
            print(f'No file exists for extensions {value}')

class ShelfScreen2(QMainWindow):
    def __init__(self):
        super(ShelfScreen2, self).__init__()
        self.dragPos = QtCore.QPoint()
        self.isMax = False

        loadUi("gui/shelf_2.ui", self)

        self.widget = None

        self.path = os.getcwd().replace('\\', '/')
        self.root_dir.setText(self.path)

        self.shelf.setIcon(QtGui.QIcon('gui/icons/ghost-solid.png'))
        self.shelf_2.setIcon(QtGui.QIcon('gui/icons/hat-wizard-solid.svg'))
        self.shelf_3.setIcon(QtGui.QIcon('gui/icons/dungeon-solid.svg'))

        self.shelf.clicked.connect(self.gotoShelf1)
        self.shelf_3.clicked.connect(self.gotoShelf3)

        self.close_btn.setIcon(QtGui.QIcon('gui/icons/x-mark.svg'))
        self.maximize_btn.setIcon(QtGui.QIcon('gui/icons/maximize.svg'))
        self.minimize_btn.setIcon(QtGui.QIcon('gui/icons/minimize.svg'))

        self.close_btn.setStyleSheet("QPushButton::hover"
                                     "{background-color : red; border-radius: 10px;}")
        self.maximize_btn.setStyleSheet("QPushButton::hover"
                                        "{background-color : green; border-radius: 5px;}")
        self.minimize_btn.setStyleSheet("QPushButton::hover"
                                        "{background-color : orange; border-radius: 5px;}")

        # self.treeView.doubleClicked.connect(self.open_file)
        self.close_btn.clicked.connect(self.app_window_controls)
        self.maximize_btn.clicked.connect(self.app_window_controls)
        self.minimize_btn.clicked.connect(self.app_window_controls)

        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.clicked.connect(self.select_item)
        # self.treeView.doubleClicked.connect(self.open_file)

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

    def startSplit(self):
        src = self.src_text_box.text()
        dest = self.dest_text_box.text()

        if os.path.exists(src):
            if os.path.exists(dest):
                self.show_popup('Warning', 'Destination Dir already exists', 'warning')
            else:
                "Starting splitting"
                ratio, ok = QInputDialog.getText(self, 'Splitting', 'Enter a split ratio')
                if ok:
                    if ratio.isnumeric() and (0 < int(ratio) < 10):

                        splitter(src, dest, int(ratio))
                        self.show_popup('Splitting ', 'Splitting Completed', 'info')
                    else:
                        self.show_popup('Splitting', 'Enter an integer between 1 to 9', 'info')
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
        self.title_bar.resize(self.width(), 40)
        self.close_btn.move(self.width() - 30, 10)
        self.maximize_btn.move(self.width() - 60, 10)
        self.minimize_btn.move(self.width() - 90, 10)

    def getWidget(self, widget):
        self.widget = widget

    def gotoShelf1(self):
        self.widget.setCurrentIndex(0)

    def gotoShelf3(self):
        self.widget.setCurrentIndex(2)

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