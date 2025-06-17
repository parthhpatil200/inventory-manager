import os
import sqlite3
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox,
                             QTableWidget, QTableWidgetItem, QScrollArea, QGroupBox)
from PySide6.QtCore import Qt, Signal

class SupplierMasterForm(QWidget):
    supplier_added = Signal()  # Signal to notify when a supplier is added
    
    def __init__(self, current_user=None):
        super().__init__()
        self.current_user = current_user
        self.setup_ui()
        self.load_suppliers()
        
    def get_db_connection(self):
        db_path = os.path.join('database', 'inventory.db')
        return sqlite3.connect(db_path)

    def setup_ui(self):
        # Create main scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # Create main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Form fields
        form_group = QGroupBox("Supplier Details")
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter supplier name")
        self.name_input.setMinimumHeight(30)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        
        # Contact Person
        contact_layout = QHBoxLayout()
        contact_label = QLabel("Contact Person:")
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Enter contact person")
        self.contact_input.setMinimumHeight(30)
        contact_layout.addWidget(contact_label)
        contact_layout.addWidget(self.contact_input)
        
        # Phone
        phone_layout = QHBoxLayout()
        phone_label = QLabel("Phone:")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number")
        self.phone_input.setMinimumHeight(30)
        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(self.phone_input)
        
        # Email
        email_layout = QHBoxLayout()
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")
        self.email_input.setMinimumHeight(30)
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        
        # Address
        address_layout = QHBoxLayout()
        address_label = QLabel("Address:")
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Enter address")
        self.address_input.setMinimumHeight(30)
        address_layout.addWidget(address_label)
        address_layout.addWidget(self.address_input)
        
        # Add all layouts to form layout
        form_layout.addLayout(name_layout)
        form_layout.addLayout(contact_layout)
        form_layout.addLayout(phone_layout)
        form_layout.addLayout(email_layout)
        form_layout.addLayout(address_layout)
        
        form_group.setLayout(form_layout)
        
        # Suppliers table
        table_group = QGroupBox("Supplier List")
        table_layout = QVBoxLayout()
        self.suppliers_table = QTableWidget()
        self.suppliers_table.setColumnCount(5)
        self.suppliers_table.setHorizontalHeaderLabels([
            "Name", "Contact Person", "Phone", "Email", "Address"
        ])
        self.suppliers_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.suppliers_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.suppliers_table.itemDoubleClicked.connect(self.load_supplier)
        self.suppliers_table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
            }
        """)
        table_layout.addWidget(self.suppliers_table)
        table_group.setLayout(table_layout)
        
        # Action buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Supplier")
        self.clear_button = QPushButton("Clear Form")
        self.save_button.setMinimumHeight(40)
        self.clear_button.setMinimumHeight(40)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)
        
        # Add all layouts to main layout
        layout.addWidget(form_group)
        layout.addWidget(table_group)
        layout.addLayout(button_layout)
        
        main_widget.setLayout(layout)
        scroll.setWidget(main_widget)
        
        # Create outer layout for scroll area
        outer_layout = QVBoxLayout()
        outer_layout.addWidget(scroll)
        self.setLayout(outer_layout)
        
        # Connect signals
        self.save_button.clicked.connect(self.save_supplier)
        self.clear_button.clicked.connect(self.clear_form)

    def load_suppliers(self):
        if not self.current_user:
            return
            
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name, contact_person, phone, email, address
            FROM suppliers
            WHERE user_id = ?
            ORDER BY name
        """, (self.current_user['id'],))
        
        suppliers = cursor.fetchall()
        self.suppliers_table.setRowCount(len(suppliers))
        
        for row, supplier in enumerate(suppliers):
            for col, value in enumerate(supplier):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.suppliers_table.setItem(row, col, item)
        
        conn.close()

    def save_supplier(self):
        if not self.current_user:
            QMessageBox.warning(self, "Error", "Please log in to save suppliers")
            return
            
        # Get values from form
        name = self.name_input.text().strip()
        contact = self.contact_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.text().strip()
        
        # Validate required fields
        if not name:
            QMessageBox.warning(self, "Error", "Please enter supplier name")
            return
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Check if supplier name already exists
            cursor.execute("SELECT id FROM suppliers WHERE name = ? AND user_id = ?", (name, self.current_user['id']))
            if cursor.fetchone():
                QMessageBox.warning(self, "Error", "Supplier name already exists")
                return
            
            # Insert new supplier
            cursor.execute("""
                INSERT INTO suppliers (
                    name, contact_person, phone, email, address, user_id
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (name, contact, phone, email, address, self.current_user['id']))
            
            conn.commit()
            QMessageBox.information(self, "Success", "Supplier saved successfully")
            self.clear_form()
            self.load_suppliers()
            self.supplier_added.emit()  # Emit signal when supplier is added
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")
        finally:
            conn.close()

    def clear_form(self):
        self.name_input.clear()
        self.contact_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.address_input.clear()

    def load_supplier(self, item):
        row = item.row()
        self.name_input.setText(self.suppliers_table.item(row, 0).text())
        self.contact_input.setText(self.suppliers_table.item(row, 1).text())
        self.phone_input.setText(self.suppliers_table.item(row, 2).text())
        self.email_input.setText(self.suppliers_table.item(row, 3).text())
        self.address_input.setText(self.suppliers_table.item(row, 4).text()) 