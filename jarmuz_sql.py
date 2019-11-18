import sys
import os
from PyQt5.QtWidgets import QApplication
import gui_objects as jarmuz

def main():
    # Clearing terminal of text
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    print("Jarmuż SQL Viewer")
    print("Cale Overstreet, 11/14/2019")
    print("\nStarting Jarmuż SQL Databases Viewer")

    app = QApplication(sys.argv)
    ex = jarmuz.App()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
