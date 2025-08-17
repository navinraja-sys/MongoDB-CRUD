from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QMessageBox, QTableWidget, QTableWidgetItem
)
from pymongo import MongoClient
from bson import ObjectId
import sys

#Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["testdb"]
collection = db["students"]

class MongoCRUD(QWidget):

    #Start GUI
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MongoDB CRUD with PyQt5 (476)")
        self.setGeometry(200, 200, 700, 400)

        layout = QVBoxLayout()
        form_layout = QHBoxLayout()

        self.roll_input = QLineEdit()
        self.name_input = QLineEdit()
        self.age_input = QLineEdit()

        form_layout.addWidget(QLabel("Roll No:"))
        form_layout.addWidget(self.roll_input)
        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel("Age:"))
        form_layout.addWidget(self.age_input)

        btn_layout = QHBoxLayout()
        insert_btn = QPushButton("Insert")
        update_btn = QPushButton("Update")
        delete_btn = QPushButton("Delete")
        refresh_btn = QPushButton("Refresh")

        insert_btn.clicked.connect(self.insert_data)
        update_btn.clicked.connect(self.update_data)
        delete_btn.clicked.connect(self.delete_data)
        refresh_btn.clicked.connect(self.load_data)

        btn_layout.addWidget(insert_btn)
        btn_layout.addWidget(update_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(refresh_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Roll No", "Name", "Age"])
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setEditTriggers(self.table.NoEditTriggers)

        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.load_data()

    #Insert
    def insert_data(self):
        roll = self.roll_input.text().strip()
        name = self.name_input.text().strip()
        age = self.age_input.text().strip()

        if roll and name and age.isdigit():
            collection.insert_one({"roll_no": roll, "name": name, "age": int(age)})
            QMessageBox.information(self, "Success", "Inserted successfully!")
            self.clear_inputs()
            self.load_data()
        else:
            QMessageBox.warning(self, "Error", "Please enter Roll No, Name and valid Age")

    #Load
    def load_data(self):
        self.table.setRowCount(0)
        for row, doc in enumerate(collection.find()):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(doc["_id"])))
            self.table.setItem(row, 1, QTableWidgetItem(doc.get("roll_no", "")))
            self.table.setItem(row, 2, QTableWidgetItem(doc.get("name", "")))
            self.table.setItem(row, 3, QTableWidgetItem(str(doc.get("age", ""))))

    #Update
    def update_data(self):
        selected = self.table.currentRow()
        if selected >= 0:
            doc_id = self.table.item(selected, 0).text()
            roll = self.roll_input.text().strip()
            name = self.name_input.text().strip()
            age = self.age_input.text().strip()
            if roll and name and age.isdigit():
                collection.update_one(
                    {"_id": ObjectId(doc_id)},
                    {"$set": {"roll_no": roll, "name": name, "age": int(age)}}
                )
                QMessageBox.information(self, "Success", "Updated successfully!")
                self.clear_inputs()
                self.load_data()
            else:
                QMessageBox.warning(self, "Error", "Enter Roll No, Name and valid Age")
        else:
            QMessageBox.warning(self, "Error", "Select a row to update")

    #Delete
    def delete_data(self):
        selected = self.table.currentRow()
        if selected >= 0:
            doc_id = self.table.item(selected, 0).text()
            collection.delete_one({"_id": ObjectId(doc_id)})
            QMessageBox.information(self, "Deleted", "Record deleted")
            self.load_data()
        else:
            QMessageBox.warning(self, "Error", "Select a row to delete")

    #Clear
    def clear_inputs(self):
        self.roll_input.clear()
        self.name_input.clear()
        self.age_input.clear()


#Run App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MongoCRUD()
    window.show()
    sys.exit(app.exec())
