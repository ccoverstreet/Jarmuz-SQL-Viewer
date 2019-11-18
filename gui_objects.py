from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QGridLayout, QWidget, QLabel, QTextEdit, QSplitter, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

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
        print("Have a nice day!")
        qApp.quit()



# Main Content Widget
class MainContentWidget(QWidget):
    def __init__(self, parent):
        super(MainContentWidget, self).__init__(parent)
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.top_section = QSplitter(Qt.Horizontal)
        self.testlabel = QLabel("Will show all databases and tables for selected database")
        self.testlabel2 = QLabel("Will hold the table output of a SQL command")
        self.testlabel.setStyleSheet("QLabel {background-color: yellow}")
        self.testlabel2.setStyleSheet("QLabel {background-color: red}")
        self.top_section.addWidget(self.testlabel)
        self.top_section.addWidget(self.testlabel2)

        self.vertical_split = QSplitter(Qt.Vertical)
        self.vertical_split.addWidget(self.top_section)
        self.vertical_split.addWidget(SQLTerminal(self))

        self.layout.addWidget(self.vertical_split, 1, 1)

        self.setLayout(self.layout)


# Interface to run SQL commands. Shows previous commands and text output. Table output will be displayed in the table viewer widget
class SQLTerminal(QWidget):
    terminal_history = []

    def __init__(self, parent):
        super(SQLTerminal, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Shows previous commands and text output
        self.terminal_output = QTextEdit()
        self.layout.addWidget(self.terminal_output)
        self.terminal_output.setReadOnly(True); # Setting to read only
        # Setting greeting for terminal
        self.terminal_output.append("Jarmuz SQL Terminal Interface")
        self.terminal_output.append("Cale Overstreet (2019)")
        self.terminal_output.append("\n")

        # Location where user inputs SQL commands
        self.terminal_input = QLineEdit()
        # self.terminal_input.installEventFilter(self)
        self.terminal_input.returnPressed.connect(self.handleUserInput)
        self.layout.addWidget(self.terminal_input)


        self.setLayout(self.layout)

    def handleUserInput(self):
        print("User input entered")
        print(self.terminal_input.text())

        if (self.terminal_input.text() == "clear"):
            self.terminal_history = []
            self.terminal_output.clear()
            self.terminal_output.setText("")
        else:
            self.terminal_output.append("<html><b>user [databasename]$</b><html> " + self.terminal_input.text())
            self.terminal_history.append(self.terminal_input.text())
            print(self.terminal_history)

        self.terminal_input.setText("")

class TerminalInputLine(QWidget):
    def __init__(self, parent):
        super(TerminalInputLine, self).__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.terminal_line = QLineEdit()
        self.layout.addWidget(self.terminal_line)

        self.setLayout(self.layout)
