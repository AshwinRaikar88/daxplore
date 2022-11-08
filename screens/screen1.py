import os
import shutil

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QMessageBox, QInputDialog, QSizePolicy


class MainScreen(QMainWindow):
    def __init__(self):
        super(MainScreen, self).__init__()
        self.setWindowIcon(QtGui.QIcon(r'C:\Users\ashwi\PycharmProjects\daxplore\gui\icons\ghost-solid.png'))

        loadUi("gui/shelf_1.ui", self)
        self.widget = None

        self.path = os.getcwd().replace('\\', '/')
        self.root_dir.setText(self.path)


        self.shelf.setIcon(QtGui.QIcon('gui/icons/ghost-solid.png'))
        self.shelf_2.setIcon(QtGui.QIcon('gui/icons/hat-wizard-solid.svg'))
        self.shelf_3.setIcon(QtGui.QIcon('gui/icons/dungeon-solid.svg'))

        self.shelf_2.clicked.connect(self.gotoShelf2)
        self.shelf_3.clicked.connect(self.gotoShelf3)

        # self.treeView.doubleClicked.connect(self.open_file)

        self.createB.clicked.connect(self.createDir)
        self.exp_back.clicked.connect(self.goBack)

        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)
        self.treeView.doubleClicked.connect(self.open_file)

        self.populate(self.path)

    def resizeEvent(self, resizeEvent):
        self.widget_1.resize(self.width(), 120)
        self.widget_2.resize(self.width(), self.height())
        self.root_dir.resize(self.width()-130, 50)
        self.action_window.resize(self.width() - 430, self.height() - 250)
        self.treeView.resize(350, self.height() - 250)

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
            self.populate(file_path)

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
            qD.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
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
        x = msg.exec_()

    def goBack(self):
        self.path = os.path.abspath(self.path + "/../").replace('\\', '/')
        self.populate(self.path)
        self.root_dir.setText(self.path)

    def populate(self, path):
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(path))
        self.treeView.setSortingEnabled(True)

    def createDir(self):
        created_flag = 0
        print(f'self.path: {self.path} + {self.dirName.text()}')
        dirNames = self.dirName.text().replace("\\", "/").split("/")

        dirName = ""
        for subdir in dirNames:
            dirName += subdir
            if dirName == "":
                self.show_popup("Alert", "Directory name cannot be empty", "warning")
                created_flag = 1
                break
            elif os.path.exists(self.path + "/" + dirName):
                dirName += "/"
            else:
                created_flag = 2
                os.mkdir(self.path + "/" + dirName)

                dirName += "/"

        # self.path = dirName
        # self.dirName.setText(self.path)
        if created_flag == 0:
            self.show_popup("Alert", "Directory already Exists", "warning")

        self.populate(self.path)

    def getWidget(self, widget):
        self.widget = widget

    def gotoShelf2(self):
        self.widget.setCurrentIndex(1)

    def gotoShelf3(self):
        self.widget.setCurrentIndex(2)
