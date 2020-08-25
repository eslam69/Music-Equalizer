from PyQt5 import QtWidgets ,QtCore, QtGui
import PyQt5.QtCore as C
from final3 import Ui_MainWindow
from popup import Ui_MainWindow2




class popWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(popWindow, self).__init__()
        self.ui = Ui_MainWindow2()
        self.ui.setupUi(self)

