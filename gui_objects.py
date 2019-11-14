from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QGridLayout, QWidget, QLabel
from PyQt5.QtGui import QIcon

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Jarmuz SQL Viewer"
        self.left = 10
        self.top = 10
        self.width = 1280
        self.height= 720
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title) #Setting window title
        self.setGeometry(self.left, self.top, self.width, self.height) # Setting geometry
        self.setContentsMargins(0, 0, 0, 0)

        # Create menubar from class function
        self.createMenubar()

        # Setting central widget
        self.setCentralWidget(MainContentWidget(self))

        self.show() # Displaying window

    def createMenubar(self):
        # Creating menu bar
        exit_option = QAction(QIcon('exit.png'), '&Exit', self)
        exit_option.setShortcut("Ctrl+Q")
        exit_option.setStatusTip("Exit Application")
        exit_option.triggered.connect(self.closeApplication)

        self.statusBar().showMessage("Ready")

        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        file_menu.addAction(exit_option)




    def closeApplication(self):
        print("\nClosing Jarmuz SQL Viewer")
        qApp.quit()



# Main Content Widget
class MainContentWidget(QWidget):
    def __init__(self, parent):
        super(MainContentWidget, self).__init__(parent)
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.testlabel = QLabel("SQL Command Line")
        self.testlabel2 = QLabel("FOASMDASDAD")
        self.testlabel.setStyleSheet("QLabel {background-color: yellow}")
        self.testlabel2.setStyleSheet("QLabel {background-color: red}")
        self.layout.addWidget(self.testlabel, 1, 1)
        self.layout.addWidget(self.testlabel2, 2, 1)

        self.setLayout(self.layout)








