from PyQt6.QtWidgets import QApplication, QBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox
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
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)  # add the sub bar to main bar

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("select * from students")
        self.table.setRowCount(0)
        for row_column, row_data in enumerate(result):
            print(row_data)
            self.table.insertRow(row_column)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_column, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        self.dialog = InsertDialog()
        self.dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        # add the student name
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        # add combo box of course
        self.courses_name = QComboBox()
        self.courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.courses_name.addItems(self.courses)
        layout.addWidget(self.courses_name)
        # add the phone number
        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText("Phone number")
        layout.addWidget(self.phone_number)

        # add submit button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course_name = self.courses_name.itemText(self.courses_name.currentIndex())
        phone_number = self.phone_number.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name,course,mobile)VALUES(?,?,?)",
                       (name, course_name, phone_number))
        connection.commit()
        cursor.close()
        connection.close()
        app_main.load_data()



app = QApplication(sys.argv)
app_main = MainWindow()
app_main.show()
app_main.load_data()
sys.exit(app.exec())
