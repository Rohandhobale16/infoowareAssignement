import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QInputDialog
)
from database import Database

class BillingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Billing System")
        self.setGeometry(200, 200, 600, 500)

        layout = QVBoxLayout()

        # Customer Inputs
        self.name_label = QLabel("Customer Name:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.phone_label = QLabel("Phone:")
        self.phone_input = QLineEdit()
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)

        self.amount_label = QLabel("Bill Amount:")
        self.amount_input = QLineEdit()
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)

        # Buttons Layout
        btn_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Bill")
        self.add_button.clicked.connect(self.add_bill)
        btn_layout.addWidget(self.add_button)

        self.view_button = QPushButton("View Bills")
        self.view_button.clicked.connect(self.view_bills)
        btn_layout.addWidget(self.view_button)

        self.edit_bill_button = QPushButton("Edit Bill")
        self.edit_bill_button.clicked.connect(self.edit_bill)
        btn_layout.addWidget(self.edit_bill_button)

        self.delete_bill_button = QPushButton("Delete Bill")
        self.delete_bill_button.clicked.connect(self.delete_bill)
        btn_layout.addWidget(self.delete_bill_button)

        layout.addLayout(btn_layout)

        # Table to display bills
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)

    def add_bill(self):
        """Adds a new bill and updates the table immediately."""
        name = self.name_input.text()
        phone = self.phone_input.text()
        amount = self.amount_input.text()

        if not name or not phone or not amount:
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return

        try:
            amount = float(amount)
            customer_id = self.db.add_customer(name, phone)
            self.db.add_bill(customer_id, amount)
            QMessageBox.information(self, "Success", "Bill Added Successfully!")

            # Clear input fields
            self.name_input.clear()
            self.phone_input.clear()
            self.amount_input.clear()

            # Automatically refresh the table
            self.view_bills()
            
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Enter a valid amount.")

    def view_bills(self):
        """Loads all bills into the table."""
        bills = self.db.get_bills()
        self.table.setRowCount(len(bills))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Customer", "Amount", "Date"])

        for row, bill in enumerate(bills):
            for col, value in enumerate(bill):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def edit_bill(self):
        """Edits the amount of a selected bill."""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a bill to edit.")
            return

        bill_id = self.table.item(selected_row, 0).text()
        new_amount, ok = QInputDialog.getText(self, "Edit Bill", "Enter new amount:")

        if ok and new_amount:
            try:
                self.db.update_bill(int(bill_id), float(new_amount))
                QMessageBox.information(self, "Success", "Bill updated successfully!")
                self.view_bills()
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Please enter a valid number.")

    def delete_bill(self):
        """Deletes a selected bill."""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a bill to delete.")
            return

        bill_id = self.table.item(selected_row, 0).text()
        confirm = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this bill?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.db.delete_bill(int(bill_id))
            QMessageBox.information(self, "Success", "Bill deleted successfully!")
            self.view_bills()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BillingApp()
    window.show()
    sys.exit(app.exec())
