import os
import sys

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow


class MainScreen(QMainWindow):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("main.ui", self)
        icon1 = QtGui.QIcon('icons/ghost-solid.png')
        self.path = os.getcwd().replace('\\', '/')

        self.shelf.setIcon(icon1)

        icon2 = QtGui.QIcon('icons/hat-wizard-solid.svg')
        self.shelf_2.setIcon(icon2)

        icon3 = QtGui.QIcon('icons/dungeon-solid.svg')
        self.shelf_3.setIcon(icon3)

        self.shelf.clicked.connect(self.setShelf)
        self.shelf_2.clicked.connect(self.setShelf_2)
        self.shelf_3.clicked.connect(self.setShelf_3)
        self.createB.clicked.connect(self.createDir)
        self.exp_back.clicked.connect(self.goBack)

        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.populate(self.path)

    def goBack(self):
        self.path = os.path.abspath(self.path + "/../").replace('\\', '/')
        self.dirName.setText(self.path)
        self.populate(self.path)
        print(self.path)

    def populate(self, path):
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(path))
        self.treeView.setSortingEnabled(True)

    def setShelf(self):
        self.label.setText("Collections")

    def setShelf_2(self):
        self.label.setText("Explore")

    def setShelf_3(self):
        self.label.setText("Home")
        self.dirName.setText(self.path)

    def createDir(self):
        dirNames = self.dirName.text().replace("\\", "/").split("/")

        dirName = ""
        for subdir in dirNames:
            dirName += subdir
            if dirName == "":
                self.dirName.setText("Directory name cannot be empty")
            elif os.path.exists(dirName):
                self.dirName.setText("Directory already exists")
                dirName += "/"
            else:
                os.mkdir(dirName)

                dirName += "/"

        self.path = dirName
        self.dirName.setText(self.path)
        self.populate(self.path)

    def gotoShelf(self):
        login = ShelfScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)


class ShelfScreen(QDialog):
    def __init__(self):
        super(ShelfScreen, self).__init__()
        loadUi("login.ui", self)
        self.shelf.clicked.connect(self.loginfunction)


# main
app = QApplication(sys.argv)
welcome = MainScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(600)
widget.setFixedWidth(800)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")

