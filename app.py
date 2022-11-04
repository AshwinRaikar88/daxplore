import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from screens.screen1 import MainScreen
from screens.screen2 import ShelfScreen2
from screens.screen3 import ShelfScreen3

# main
# app = QApplication(sys.argv)
app = QApplication([])

sh1 = MainScreen()
sh2 = ShelfScreen2()
sh3 = ShelfScreen3()


widget = QtWidgets.QStackedWidget()

widget.addWidget(sh1)
widget.addWidget(sh2)
widget.addWidget(sh3)

sh1.getWidget(widget)
sh2.getWidget(widget)
sh3.getWidget(widget)
# widget.setFixedHeight(600)
# widget.setFixedWidth(800)

widget.show()


try:
    sys.exit(app.exec_())
except:
    print("Exiting")

