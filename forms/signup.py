import sqlite3
import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Qt

class SignupWindow(QWidget):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.setup_ui()

    def get_db_connection(self):
        db_path = os.path.join('database', 'inventory.db')
        return sqlite3.connect(db_path)

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        
        # Email
        email_layout = QHBoxLayout()
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        
        # Full Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Full Name:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        
        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        # Confirm Password
        confirm_layout = QHBoxLayout()
        confirm_label = QLabel("Confirm Password:")
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.Password)
        confirm_layout.addWidget(confirm_label)
        confirm_layout.addWidget(self.confirm_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        signup_button = QPushButton("Sign Up")
        cancel_button = QPushButton("Cancel")
        signup_button.clicked.connect(self.signup)
        cancel_button.clicked.connect(self.cancel)
        button_layout.addWidget(signup_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(username_layout)
        layout.addLayout(email_layout)
        layout.addLayout(name_layout)
        layout.addLayout(password_layout)
        layout.addLayout(confirm_layout)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.setWindowTitle("Sign Up")
        self.setFixedSize(300, 200)

    def signup(self):
        # Get values from form
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        name = self.name_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        # Validate required fields
        if not all([username, email, name, password, confirm]):
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
        
        # Validate email format
        if '@' not in email or '.' not in email:
            QMessageBox.warning(self, "Error", "Please enter a valid email address")
            return
        
        # Validate password match
        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return
        
        # Validate password length
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters long")
            return
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Check if username or email already exists
            cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
            if cursor.fetchone():
                QMessageBox.warning(self, "Error", "Username or email already exists")
                return
            
            # Insert new user
            cursor.execute('''
                INSERT INTO users (username, password, email, name)
                VALUES (?, ?, ?, ?)
            ''', (username, password, email, name))
            
            conn.commit()
            QMessageBox.information(self, "Success", "Account created successfully. Please log in.")
            self.close()
            self.login_window.show()
            
        except sqlite3.Error as e:
            error_msg = str(e)
            if "no such table" in error_msg.lower():
                QMessageBox.critical(self, "Error", "Database tables not created. Please restart the application.")
            else:
                QMessageBox.critical(self, "Error", f"Database error: {error_msg}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def cancel(self):
        self.close()
        self.login_window.show() 