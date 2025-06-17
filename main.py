import sys
import sqlite3
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QMessageBox, QStackedWidget, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont

from forms.goods_receiving import GoodsReceivingForm
from forms.sales_form import SalesForm
from forms.product_master import ProductMasterForm
from forms.supplier_master import SupplierMasterForm
from forms.customer_master import CustomerMasterForm
from forms.signup import SignupWindow
from database.db_setup import setup_database
from styles import MAIN_WINDOW_STYLE, NAV_BUTTON_STYLE, FORM_STYLE

class LoginWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
        self.setStyleSheet(MAIN_WINDOW_STYLE)

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title_label = QLabel("Inventory Management System")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        
        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        login_button = QPushButton("Login")
        signup_button = QPushButton("Sign Up")
        login_button.setStyleSheet(NAV_BUTTON_STYLE)
        signup_button.setStyleSheet(NAV_BUTTON_STYLE)
        login_button.clicked.connect(self.login)
        signup_button.clicked.connect(self.show_signup)
        button_layout.addWidget(login_button)
        button_layout.addWidget(signup_button)
        
        # Add all widgets to main layout
        layout.addWidget(title_label)
        layout.addSpacing(20)
        layout.addLayout(username_layout)
        layout.addLayout(password_layout)
        layout.addSpacing(20)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.setWindowTitle("Login")
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
            }
        """)

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
        self.setStyleSheet(MAIN_WINDOW_STYLE)

    def setup_database(self):
        # Always call setup_database to ensure tables are created
        setup_database()

    def setup_ui(self):
        self.setWindowTitle("Inventory Management System")
        self.setMinimumSize(1200, 800)
        
        # Create central widget with main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create navigation bar
        nav_frame = QFrame()
        nav_frame.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                padding: 10px;
            }
        """)
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(10)
        nav_layout.setContentsMargins(20, 10, 20, 10)
        
        # Navigation buttons
        self.goods_receiving_btn = QPushButton("Goods Receiving")
        self.sales_btn = QPushButton("Sales")
        self.product_master_btn = QPushButton("Product Master")
        self.supplier_master_btn = QPushButton("Supplier Master")
        self.customer_master_btn = QPushButton("Customer Master")
        
        # Set button styles
        for btn in [self.goods_receiving_btn, self.sales_btn, self.product_master_btn,
                   self.supplier_master_btn, self.customer_master_btn]:
            btn.setStyleSheet(NAV_BUTTON_STYLE)
        
        # Connect buttons
        self.goods_receiving_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.sales_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.product_master_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.supplier_master_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.customer_master_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        
        # Add buttons to nav layout
        nav_layout.addWidget(self.goods_receiving_btn)
        nav_layout.addWidget(self.sales_btn)
        nav_layout.addWidget(self.product_master_btn)
        nav_layout.addWidget(self.supplier_master_btn)
        nav_layout.addWidget(self.customer_master_btn)
        nav_layout.addStretch()
        
        nav_frame.setLayout(nav_layout)
        
        # Create stacked widget for different forms
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet(FORM_STYLE)
        
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
        
        # Add widgets to main layout
        main_layout.addWidget(nav_frame)
        main_layout.addWidget(self.stacked_widget)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

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
        self.goods_receiving_form.load_receiving_list()
        self.sales_form.load_products()
        self.sales_form.load_customers()
        self.sales_form.load_sales_list()
        
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec()) 