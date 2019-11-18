from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QGridLayout, QWidget, QLabel, QTextEdit, QSplitter, QLineEdit, QHBoxLayout, QVBoxLayout, QTableWidget,QTableWidgetItem
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import mysql.connector as sql

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Jarmuz SQL Viewer"
        self.left = 400
        self.top = 300
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
        self.sql_table = SQLTableDisplay(self)
        self.top_section.addWidget(self.sql_table)

        self.vertical_split = QSplitter(Qt.Vertical)
        self.vertical_split.addWidget(self.top_section)
        self.sql_terminal = SQLTerminal(self)
        self.vertical_split.addWidget(self.sql_terminal)

        self.layout.addWidget(self.vertical_split, 1, 1)

        self.setLayout(self.layout)

    def updateTable(self, table_data, column_names):
        self.sql_table.updateTable(table_data, column_names)


# Interface to run SQL commands. Shows previous commands and text output. Table output will be displayed in the table viewer widget
class SQLTerminal(QWidget):
    terminal_history = []
    terminal_index = 0

    user = "coverst2"
    password = "Heuristics11!"

    connection = sql.connect(user=user, password=password)
    cursor = connection.cursor()
    selected_database = ""



    def __init__(self, parent):
        self.parent = parent
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

    # Key handling for command history
    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Up: # When up key is pressed
            if (self.terminal_index > 0): # If the index is not at the earliest entry
                self.terminal_index -= 1
                self.terminal_input.setText(self.terminal_history[self.terminal_index]) # Set text to current index
        elif key == Qt.Key_Down: # When down key is pressed
            if (self.terminal_index < len(self.terminal_history)): # If the index is not at the last entry
                self.terminal_index += 1

                if (self.terminal_index != len(self.terminal_history)): # If the current index is not the current entry line
                    self.terminal_input.setText(self.terminal_history[self.terminal_index]) # Set text to current index
                else:
                    self.terminal_input.setText("")


    def handleUserInput(self):
        user_command = self.terminal_input.text()

        if (user_command == "clear"): # Command to clear SQL Command Window
            self.terminal_history.append(user_command)
            self.terminal_index = len(self.terminal_history)
            self.terminal_output.setText("")
        elif (user_command == "exit"): # Command to close app
            qApp.quit()
        elif (self.terminal_input.text() == "test"):
            self.parent.updateTable("Hi")
        else:
            self.terminal_output.append("<html><b>user [databasename]$</b><html> " + user_command)
            self.terminal_history.append(user_command)
            self.terminal_index = len(self.terminal_history)
            print(self.terminal_history)

            # Execute SQL command and catch errors

            if ("USE" in user_command or "use" in user_command):
                self.selected_database = user_command.split()[1]
                self.cursor.execute(user_command)
            elif (self.selected_database != ""):
                self.cursor.execute(user_command)
                output_table = self.cursor.fetchall()
                print(self.cursor.column_names)
                self.parent.updateTable(output_table, self.cursor.column_names)
            else:
                self.terminal_output.append("Please select a database")

        self.terminal_input.setText("")


class SQLTableDisplay(QWidget):
    def __init__(self, parent):
        super(SQLTableDisplay, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.sql_table = QTableWidget()
        self.sql_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.sql_table.setRowCount(1)
        self.sql_table.setColumnCount(1)

        self.sql_table.setItem(0, 0, QTableWidgetItem("No Table Selected"))

        self.sql_table.resizeColumnsToContents()

        self.layout.addWidget(self.sql_table)

        self.setLayout(self.layout)

    def updateTable(self, table_data, column_names):
        self.sql_table.setItem(0, 0, QTableWidgetItem(str(len(table_data))))
        self.sql_table.setRowCount(len(table_data))
        self.sql_table.setColumnCount(len(table_data[0]))

        column_labels = []
        for i in range(0, len(column_names)):
            column_labels.append(column_names[i])

        self.sql_table.setHorizontalHeaderLabels(column_labels)

        for i in range(0, len(table_data)):
            for j in range(0, len(table_data[0])):
                self.sql_table.setItem(i, j, QTableWidgetItem(str(table_data[i][j])))
        print(table_data)
