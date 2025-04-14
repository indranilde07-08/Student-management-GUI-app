from PyQt6.QtWidgets import QApplication, QBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(500, 500)

        file_menu_item = self.menuBar().addMenu("&File")  # create menu bar
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/icons/add.png"), "Add Student", self)  # create sub bar
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)  # add the sub bar to main bar

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        search_student_action = QAction(QIcon("icons/icons/search.png"), "Search student", self)
        search_student_action.triggered.connect(self.insert_search)
        edit_menu_item.addAction(search_student_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        # create toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)

        # Create status bar and status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect the automatically clik button
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

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

    def insert_search(self):
        self.dialog_search = SearchDialog()
        self.dialog_search.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        # add the student name
        layout = QVBoxLayout()
        # Get student name from selected row
        index = app_main.table.currentRow()
        student_name = app_main.table.item(index, 1).text()
        self.student_id = app_main.table.item(index, 0).text()
        # Add student name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        # add combo box of course
        course_names = app_main.table.item(index, 2).text()
        self.courses_name = QComboBox()
        self.courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.courses_name.addItems(self.courses)
        self.courses_name.setCurrentText(course_names)
        layout.addWidget(self.courses_name)
        # add the phone number
        phone_number = app_main.table.item(index, 3).text()
        self.phone_number = QLineEdit(phone_number)
        self.phone_number.setPlaceholderText("Phone number")
        layout.addWidget(self.phone_number)

        # add submit button
        button = QPushButton("update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("update students set name= ?,course=?,mobile= ? where id= ? ",
                       (self.student_name.text(),
                        self.courses_name.itemText(self.courses_name.currentIndex()),
                        self.phone_number.text(),self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        #Refresh the table
        app_main.load_data()


class DeleteDialog(QDialog):
    pass


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
        name = self.student_name.text().strip()
        course_name = self.courses_name.itemText(self.courses_name.currentIndex()).strip()
        phone_number = self.phone_number.text().strip()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name,course,mobile)VALUES(?,?,?)",
                       (name, course_name, phone_number))
        connection.commit()
        cursor.close()
        connection.close()
        app_main.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student name Search")
        self.setFixedWidth(400)
        self.setFixedHeight(400)
        layout = QVBoxLayout()
        self.student_search_name = QLineEdit()
        self.student_search_name.setPlaceholderText("Name")
        layout.addWidget(self.student_search_name)
        button = QPushButton("Search")
        button.clicked.connect(self.student_search)
        layout.addWidget(button)
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)

    def student_search(self):
        name = self.student_search_name.text().strip()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("select * from students where name=?", (name,))
        result = result.fetchall()
        self.table.setRowCount(0)
        self.table.setColumnCount(len(result[0]))
        header = [desc[0] for desc in cursor.description]
        self.table.setHorizontalHeaderLabels(header)
        for row_column, row_data in enumerate(result):
            print(row_data)
            self.table.insertRow(row_column)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_column, column_number, QTableWidgetItem(str(data)))
        cursor.close()
        connection.close()


app = QApplication(sys.argv)
app_main = MainWindow()
app_main.show()
app_main.load_data()
sys.exit(app.exec())
