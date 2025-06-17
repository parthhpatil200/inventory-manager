import sys
import sqlite3
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QMessageBox, QStackedWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from forms.goods_receiving import GoodsReceivingForm
from forms.sales_form import SalesForm
from forms.product_master import ProductMasterForm
from forms.supplier_master import SupplierMasterForm
from forms.customer_master import CustomerMasterForm
from forms.signup import SignupWindow
from database.db_setup import setup_database

class LoginWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        
        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        # Login button
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        
        # Signup button
        signup_button = QPushButton("Sign Up")
        signup_button.clicked.connect(self.show_signup)
        
        layout.addLayout(username_layout)
        layout.addLayout(password_layout)
        layout.addWidget(login_button)
        layout.addWidget(signup_button)
        
        self.setLayout(layout)
        self.setWindowTitle("Login")
        self.setFixedSize(300, 150)

    def get_db_connection(self):
        db_path = os.path.join('database', 'inventory.db')
        return sqlite3.connect(db_path)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, username, name FROM users WHERE username = ? AND password = ?",
                      (username, password))
        user = cursor.fetchone()
        
        conn.close()
        
        if user:
            self.main_window.current_user = {
                'id': user[0],
                'username': user[1],
                'name': user[2]
            }
            self.main_window.show_main_interface()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")

    def show_signup(self):
        self.signup_window = SignupWindow(self)
        self.signup_window.show()
        self.hide()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.setup_database()
        self.setup_ui()
        self.show_login()

    def setup_database(self):
        # Always call setup_database to ensure tables are created
        setup_database()

    def setup_ui(self):
        self.setWindowTitle("Inventory Management System")
        self.setMinimumSize(1200, 800)
        
        # Create stacked widget for different forms
        self.stacked_widget = QStackedWidget()
        
        # Create navigation buttons
        nav_layout = QHBoxLayout()
        self.goods_receiving_btn = QPushButton("Goods Receiving")
        self.sales_btn = QPushButton("Sales")
        self.product_master_btn = QPushButton("Product Master")
        self.supplier_master_btn = QPushButton("Supplier Master")
        self.customer_master_btn = QPushButton("Customer Master")
        
        self.goods_receiving_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.sales_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.product_master_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.supplier_master_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.customer_master_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        
        nav_layout.addWidget(self.goods_receiving_btn)
        nav_layout.addWidget(self.sales_btn)
        nav_layout.addWidget(self.product_master_btn)
        nav_layout.addWidget(self.supplier_master_btn)
        nav_layout.addWidget(self.customer_master_btn)
        
        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.stacked_widget)
        
        # Create central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Add forms to stacked widget
        self.product_master_form = ProductMasterForm(self.current_user)
        self.supplier_master_form = SupplierMasterForm(self.current_user)
        self.customer_master_form = CustomerMasterForm(self.current_user)
        self.goods_receiving_form = GoodsReceivingForm(self.product_master_form, self.current_user)
        self.sales_form = SalesForm(self.product_master_form, self.current_user)
        
        # Connect signals
        self.supplier_master_form.supplier_added.connect(self.goods_receiving_form.load_suppliers)
        self.customer_master_form.customer_added.connect(self.sales_form.load_customers)
        
        self.stacked_widget.addWidget(self.goods_receiving_form)
        self.stacked_widget.addWidget(self.sales_form)
        self.stacked_widget.addWidget(self.product_master_form)
        self.stacked_widget.addWidget(self.supplier_master_form)
        self.stacked_widget.addWidget(self.customer_master_form)

    def show_login(self):
        self.login_window = LoginWindow(self)
        self.login_window.show()
        self.hide()

    def show_main_interface(self):
        # Update forms with current user
        self.product_master_form.current_user = self.current_user
        self.supplier_master_form.current_user = self.current_user
        self.customer_master_form.current_user = self.current_user
        self.goods_receiving_form.current_user = self.current_user
        self.sales_form.current_user = self.current_user
        
        # Refresh data
        self.product_master_form.load_categories()
        self.product_master_form.load_products()
        self.supplier_master_form.load_suppliers()
        self.customer_master_form.load_customers()
        self.goods_receiving_form.load_products()
        self.goods_receiving_form.load_suppliers()
        self.sales_form.load_products()
        self.sales_form.load_customers()
        
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec()) 