from PyQt6.QtWidgets import QApplication, QBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget,QTableWidgetItem
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")  # create menu bar
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)  # create sub bar
        file_menu_item.addAction(add_student_action)  # add the sub bar to main bar

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.setCentralWidget(self.table)
    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("select * from students")
        self.table.setRowCount(0)
        for row_column,row_data in enumerate(result):
            print(row_data)
            self.table.insertRow(row_column)
            for column_number,data in enumerate(row_data):
                self.table.setItem(row_column,column_number,QTableWidgetItem(str(data)))
                print(column_number)





app = QApplication(sys.argv)
app_main = MainWindow()
app_main.show()
app_main.load_data()
sys.exit(app.exec())
