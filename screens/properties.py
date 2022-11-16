import os

from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication

from showinfm import show_in_file_manager


class Properties(QDialog):
    def __init__(self, fileName="Default", filePath="", dir="d"):
        super(QDialog, self).__init__()
        loadUi("gui/properties.ui", self)

        self.dir_type = dir
        self.filepath.setText(filePath)
        self.clipboard = QApplication.clipboard()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowIcon(QtGui.QIcon('gui/icons/ghost-solid.svg'))

        self.filename.setText(fileName)
        self.copy.setIcon(QtGui.QIcon('gui/icons/normal.svg'))
        self.open_exp.setIcon(QtGui.QIcon('gui/icons/goto.svg'))

        if dir == "d":
            self.shelf.setIcon(QtGui.QIcon('gui/icons/file_icons/folder.svg'))
            self.shelf.setStyleSheet("background-color : rgb(248, 222, 126); border-radius: 10px;")
        elif dir == "e":
            self.shelf.setIcon(QtGui.QIcon('gui/icons/file_icons/image-solid.svg'))
            self.shelf.setStyleSheet("background-color : rgb(255, 54, 94); border-radius: 10px;")
        elif dir == "t":
            self.shelf.setIcon(QtGui.QIcon('gui/icons/file_icons/txt_file.svg'))
            self.shelf.setStyleSheet("background-color : rgb(245, 245, 245); border-radius: 10px;")
        elif dir == "f":
            self.shelf.setIcon(QtGui.QIcon('gui/icons/ghost-solid.png'))
            self.shelf.setStyleSheet("background-color : rgb(241, 213, 146); border-radius: 10px;")

        self.close_btn.setIcon(QtGui.QIcon('gui/icons/x-mark.svg'))
        self.close_btn.setStyleSheet("QPushButton::hover"
                                     "{background-color : red; border-radius: 10px;}")

        self.copy.clicked.connect(self.copy_to_clipboard)
        self.open_exp.clicked.connect(self.open_in_explorer)
        self.close_btn.clicked.connect(self.close)

    def open_in_explorer(self):
        if self.dir_type != "d":
            show_in_file_manager(os.path.abspath(self.filepath.text()+"/../"))
        else:
            show_in_file_manager(self.filepath.text())

    def copy_to_clipboard(self):
        self.clipboard.setText(self.filepath.text())
        self.show_popup("Daxplore", f"Path copied to clipboard", "info")

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

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self.title_bar.underMouse():
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()
