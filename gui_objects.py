from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QGridLayout, QWidget, QLabel, QTextEdit, QSplitter, QLineEdit, QHBoxLayout, QVBoxLayout, QTableWidget,QTableWidgetItem, QDialog, QPushButton
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import mysql.connector as sql

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Jarmuż SQL Viewer"
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

        self.main_widget = MainContentWidget(self)

        # Setting central widget
        self.setCentralWidget(self.main_widget)

        self.show() # Displaying window

    def createMenubar(self):
        # Creating menu bar
        exit_option = QAction(QIcon('exit.png'), 'Exit Jarmuż', self)
        exit_option.setShortcut("Ctrl+Q")
        exit_option.setStatusTip("Exit Application")
        exit_option.triggered.connect(self.closeApplication)

        login_option = QAction(QIcon('none'), 'Login', self)
        login_option.setShortcut("Ctrl+L")
        login_option.triggered.connect(self.loginSQL)

        self.statusBar().showMessage("Ready")

        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        file_menu.addAction(exit_option)
        file_menu.addAction(login_option)


        self.login_dialog = LoginDialog(self)
        self.login_dialog.hide()




    def closeApplication(self):
        print("\nClosing Jarmuż SQL Viewer")
        print("Have a nice day!")
        qApp.quit()

    def loginSQL(self):
        self.login_dialog.show()


    def passLoginToSQLTerminal(self, username, cursor):
        self.main_widget.passLoginInfo(username, cursor)


# Login Dialog
class LoginDialog(QDialog):
    def __init__(self, parent):
        self.parent = parent
        super(LoginDialog, self).__init__()
        self.layout = QVBoxLayout()

        self.entry_grid = QGridLayout()

        # Grouping for getting username
        self.username_label = QLabel("Username")
        self.entry_grid.addWidget(self.username_label, 0, 0)
        self.username_entry = QLineEdit()
        self.entry_grid.addWidget(self.username_entry, 0, 1)


        # Grouping for getting password
        self.password_label = QLabel("Password")
        self.entry_grid.addWidget(self.password_label, 1, 0)
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.entry_grid.addWidget(self.password_entry, 1, 1)

        self.layout.addLayout(self.entry_grid)

        self.button_layout = QHBoxLayout()
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.loginProcess)
        self.button_layout.addWidget(self.login_button)

        self.close_button = QPushButton("Cancel")
        self.button_layout.addWidget(self.close_button)
        self.layout.addLayout(self.button_layout)


        self.setLayout(self.layout)

        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def loginProcess(self):
        try:
            self.connection = sql.connect(user=self.username_entry.text(), password=self.password_entry.text())
            self.connection.autocommit = True
            cursor = self.connection.cursor()
            self.parent.passLoginToSQLTerminal(self.username_entry.text(), cursor)
        except Exception as err:
            print(err)

            label = QLabel("Incorrect username or password")
            label.setStyleSheet("QLabel {color: red}")
            self.entry_grid.addWidget(label, 2, 0, 1, 2)
        else:
            self.close()



# Main Content Widget
class MainContentWidget(QWidget):
    def __init__(self, parent):
        super(MainContentWidget, self).__init__(parent)
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.top_section = QSplitter(Qt.Horizontal)

        self.user_databases_table = DatabaseTableDisplay(self)
        self.top_section.addWidget(self.user_databases_table)

        self.tables_table = TablesInDatabaseDisplay(self)
        self.top_section.addWidget(self.tables_table)

        self.sql_table = SQLTableDisplay(self)
        self.top_section.addWidget(self.sql_table)

        self.top_section.setStretchFactor(0, 2)
        self.top_section.setStretchFactor(1, 2)
        self.top_section.setStretchFactor(2, 7)

        self.vertical_split = QSplitter(Qt.Vertical)
        self.vertical_split.addWidget(self.top_section)
        self.sql_terminal = SQLTerminal(self)
        self.vertical_split.addWidget(self.sql_terminal)

        self.vertical_split.setStretchFactor(0, 6)
        self.vertical_split.setStretchFactor(1, 1)

        self.layout.addWidget(self.vertical_split, 1, 1)

        self.setLayout(self.layout)

    def updateQueryTable(self, table_data, column_names):
        self.sql_table.updateTable(table_data, column_names)

    def updateUserDatabases(self, database_names):
        self.user_databases_table.updateTable(database_names, ["Databases"])

    def updateTablesInDatabase(self, table_names):
        self.tables_table.updateTable(table_names, ["Tables"])

    def passDatabaseTableIndex(self, clicked_index):
        self.sql_terminal.executeSQLCommand("USE " + clicked_index)

    def passTablesInDatabaseIndex(self, clicked_index):
        self.sql_terminal.executeSQLCommand("SELECT * FROM " + clicked_index)

    def passLoginInfo(self, username, cursor):
        self.sql_terminal.loginToDatabase(username, cursor)


# Interface to run SQL commands. Shows previous commands and text output. Table output will be displayed in the table viewer widget
class SQLTerminal(QWidget):
    terminal_history = []
    terminal_index = 0

    cursor = 0
    username = "none"


    selected_database = "none"

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
        self.terminal_output.append("Jarmuż SQL Terminal Interface")
        self.terminal_output.append("Cale Overstreet (2019)")
        self.terminal_output.append("\n")
        self.terminal_output.append("<html><b>{} [{}]$</b><html> ".format(self.username, self.selected_database))

        # Location where user inputs SQL commands
        self.terminal_input = QLineEdit()
        # self.terminal_input.installEventFilter(self)
        self.terminal_input.returnPressed.connect(self.handleUserInput)
        self.layout.addWidget(self.terminal_input)


        self.setLayout(self.layout)

    def loginToDatabase(self, username, cursor):
        self.username = username
        self.cursor = cursor

        self.terminal_output.moveCursor(QTextCursor.End)
        self.terminal_output.insertPlainText("Login")
        self.terminal_output.append("<html><b>{} [{}]$</b><html> ".format(self.username, self.selected_database))

        self.updateUserDatabases()

    def updateUserDatabases(self):
        self.cursor.execute("SHOW DATABASES")
        self.parent.updateUserDatabases(self.cursor.fetchall())

    def updateTablesInDatabase(self):
        self.cursor.execute("SHOW TABLES")
        self.parent.updateTablesInDatabase(self.cursor.fetchall())

    def updateTablesInDatabaseWithIndex(self, clicked_index):
        if (self.cursor == 0):
            return

        self.cursor.execute("USE " + clicked_index)
        self.updateTablesInDatabase()

    def updateQueryTable(self, table_name):
        self.cursor.execute("SELECT * FROM " + table_name)
        column_names = self.cursor.column_names
        table_data = self.cursor.fetchall()

        self.parent.updateQueryTable(table_data, column_names)

    def updateQueryTableWithIndex(self, clicked_index):
        if (self.cursor == 0):
            return
        self.updateQueryTable(clicked_index)

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
        user_command = self.terminal_input.text().strip()
        self.terminal_input.setText("")

        if len(self.terminal_history) > 0 and str(user_command) == str(self.terminal_history[-1]): # Don't add command to history if it is the same command
            None
        else:
            self.terminal_history.append(user_command)

        self.terminal_index = len(self.terminal_history) # Setting index to new position

        if (user_command == "clear"): # Command to clear SQL Command Window
            self.terminal_output.setText("")
        elif (user_command == "exit"): # Command to close app
            qApp.quit()
        elif (self.terminal_input.text() == "test"):
            self.parent.updateTable("Hi")
        else:

            if (self.cursor == 0):
                self.terminal_output.moveCursor(QTextCursor.End)
                self.terminal_output.insertPlainText(user_command)
                self.terminal_output.append("<html><div style='color: red;'>Please login to SQL database using Ctrl+L or clicking on the 'File' menu</div></html>")
                self.terminal_output.append("<html><b>{} [{}]$</b><html> ".format(self.username, self.selected_database))
                return

            # Execute SQL command and catch errors
            self.executeSQLCommand(user_command)


    def executeSQLCommand(self, sql_command):
        self.terminal_output.moveCursor(QTextCursor.End)
        self.terminal_output.insertPlainText(sql_command)

        try:
            self.cursor.execute(sql_command)
        except sql.Error as err:
            self.terminal_output.append("")
            self.terminal_output.append("<html><div style='color: red;'>Error Code [{}]</div></html>".format(err.errno))
            self.terminal_output.append("<html><div style='color: red;'>SQL STATE [{}]</div></html>".format(err.sqlstate))
            self.terminal_output.append("<html><div style='color: red;'>{}</div></html>".format(err.msg))
            self.terminal_output.append("")
        else:
            if ("use" in sql_command.lower() and len(sql_command.split()) == 2):
                self.selected_database = sql_command.split()[1]


        if self.cursor.with_rows:
            sql_column_names = self.cursor.column_names
            sql_result = self.cursor.fetchall()
            self.parent.updateQueryTable(sql_result, sql_column_names)

        self.terminal_output.append("<html><b>{} [{}]$</b><html> ".format(self.username, self.selected_database))

        if ("use" in sql_command.lower()):
            self.updateTablesInDatabase()
        if ("insert " in sql_command.lower() or "delete " in sql_command.lower()):
            table_name = sql_command.split()[2]
            self.updateQueryTable(table_name)
        if ("update " in sql_command.lower()):
            table_name = sql_command.split()[1]
            self.updateQueryTable(table_name)

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
        if (len(table_data) > 0):
            self.sql_table.setRowCount(len(table_data))
            self.sql_table.setColumnCount(len(table_data[0]))

            column_labels = []
            for i in range(0, len(column_names)):
                column_labels.append(str(column_names[i]))

            self.sql_table.setHorizontalHeaderLabels(column_labels)

            for i in range(0, len(table_data)):
                for j in range(0, len(table_data[0])):
                    self.sql_table.setItem(i, j, QTableWidgetItem(str(table_data[i][j])))
        else:
            self.sql_table.setRowCount(1)
            self.sql_table.setColumnCount(1)

            self.sql_table.setItem(0, 0, QTableWidgetItem("Nothing"))

class DatabaseTableDisplay(QWidget):
    def __init__(self, parent):
        self.parent = parent
        super(DatabaseTableDisplay, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.database_table = QTableWidget()
        self.database_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.database_table.setRowCount(1)
        self.database_table.setColumnCount(1)
        self.database_table.clicked.connect(self.databaseTableClicked)

        self.database_table.setItem(0, 0, QTableWidgetItem("No Databases"))
        self.database_table.resizeColumnsToContents()
        self.layout.addWidget(self.database_table)

        self.setLayout(self.layout)

    def databaseTableClicked(self, clicked_index):
        self.parent.passDatabaseTableIndex(str(clicked_index.data()))

    def updateTable(self, table_data, column_names):
        if (len(table_data) > 0):
            self.database_table.setRowCount(len(table_data))
            self.database_table.setColumnCount(len(table_data[0]))

            column_labels = []
            for i in range(0, len(column_names)):
                column_labels.append(str(column_names[i]))

            self.database_table.setHorizontalHeaderLabels(column_labels)

            for i in range(0, len(table_data)):
                for j in range(0, len(table_data[0])):
                    self.database_table.setItem(i, j, QTableWidgetItem(str(table_data[i][j])))
        else:
            self.database_table.setRowCount(1)
            self.database_table.setColumnCount(1)

            self.database_table.setItem(0, 0, QTableWidgetItem("Nothing"))



class TablesInDatabaseDisplay(QWidget):
    def __init__(self, parent):
        self.parent = parent

        super(TablesInDatabaseDisplay, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tables_table = QTableWidget()
        self.tables_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tables_table.setRowCount(1)
        self.tables_table.setColumnCount(1)
        self.tables_table.clicked.connect(self.tableClicked)

        self.tables_table.setItem(0, 0, QTableWidgetItem("No Databases"))
        self.tables_table.resizeColumnsToContents()
        self.layout.addWidget(self.tables_table)

        self.setLayout(self.layout)

    def tableClicked(self, clicked_index):
        self.parent.passTablesInDatabaseIndex(clicked_index.data())

    def updateTable(self, table_data, column_names):
        if (len(table_data) > 0):
            self.tables_table.setRowCount(len(table_data))
            self.tables_table.setColumnCount(len(table_data[0]))

            column_labels = []
            for i in range(0, len(column_names)):
                column_labels.append(str(column_names[i]))

            self.tables_table.setHorizontalHeaderLabels(column_labels)

            for i in range(0, len(table_data)):
                for j in range(0, len(table_data[0])):
                    self.tables_table.setItem(i, j, QTableWidgetItem(str(table_data[i][j])))
        else:
            self.tables_table.setRowCount(1)
            self.tables_table.setColumnCount(1)

            self.tables_table.setItem(0, 0, QTableWidgetItem("Nothing"))



