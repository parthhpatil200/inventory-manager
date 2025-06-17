import os
import sqlite3
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QComboBox, QTextEdit, QPushButton,
                             QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QImage
import qrcode
from PIL import Image

class ProductMasterForm(QWidget):
    # Signal to notify when a new product is added
    product_added = Signal()
    
    def __init__(self, current_user=None):
        super().__init__()
        self.current_user = current_user
        self.setup_ui()
        self.load_categories()
        self.load_products()
        self.current_image_path = None

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Product Details Section
        details_layout = QHBoxLayout()
        
        # Left side - Basic details
        left_layout = QVBoxLayout()
        
        # Barcode
        barcode_layout = QHBoxLayout()
        barcode_label = QLabel("Barcode:")
        self.barcode_input = QLineEdit()
        barcode_layout.addWidget(barcode_label)
        barcode_layout.addWidget(self.barcode_input)
        
        # SKU ID
        sku_layout = QHBoxLayout()
        sku_label = QLabel("SKU ID:")
        self.sku_input = QLineEdit()
        sku_layout.addWidget(sku_label)
        sku_layout.addWidget(self.sku_input)
        
        # Category
        category_layout = QHBoxLayout()
        category_label = QLabel("Category:")
        self.category_combo = QComboBox()
        self.category_combo.setEditable(True)
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        
        # Subcategory
        subcategory_layout = QHBoxLayout()
        subcategory_label = QLabel("Subcategory:")
        self.subcategory_combo = QComboBox()
        self.subcategory_combo.setEditable(True)
        subcategory_layout.addWidget(subcategory_label)
        subcategory_layout.addWidget(self.subcategory_combo)
        
        # Product Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Product Name:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        
        # Description
        desc_layout = QVBoxLayout()
        desc_label = QLabel("Description:")
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_input)
        
        # Tax Rate
        tax_layout = QHBoxLayout()
        tax_label = QLabel("Tax Rate (%):")
        self.tax_input = QLineEdit()
        tax_layout.addWidget(tax_label)
        tax_layout.addWidget(self.tax_input)
        
        # Price
        price_layout = QHBoxLayout()
        price_label = QLabel("Price:")
        self.price_input = QLineEdit()
        price_layout.addWidget(price_label)
        price_layout.addWidget(self.price_input)
        
        # Default Unit
        unit_layout = QHBoxLayout()
        unit_label = QLabel("Default Unit:")
        self.unit_input = QLineEdit()
        unit_layout.addWidget(unit_label)
        unit_layout.addWidget(self.unit_input)
        
        # Add all layouts to left side
        left_layout.addLayout(barcode_layout)
        left_layout.addLayout(sku_layout)
        left_layout.addLayout(category_layout)
        left_layout.addLayout(subcategory_layout)
        left_layout.addLayout(name_layout)
        left_layout.addLayout(desc_layout)
        left_layout.addLayout(tax_layout)
        left_layout.addLayout(price_layout)
        left_layout.addLayout(unit_layout)
        
        # Right side - Image
        right_layout = QVBoxLayout()
        
        # Image preview
        self.image_label = QLabel()
        self.image_label.setFixedSize(300, 300)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid #ccc;")
        
        # Image buttons
        image_buttons_layout = QHBoxLayout()
        self.browse_button = QPushButton("Browse Image")
        self.browse_button.clicked.connect(self.browse_image)
        self.clear_image_button = QPushButton("Clear Image")
        self.clear_image_button.clicked.connect(self.clear_image)
        
        image_buttons_layout.addWidget(self.browse_button)
        image_buttons_layout.addWidget(self.clear_image_button)
        
        right_layout.addWidget(self.image_label)
        right_layout.addLayout(image_buttons_layout)
        right_layout.addStretch()
        
        # Add left and right layouts to details layout
        details_layout.addLayout(left_layout)
        details_layout.addLayout(right_layout)
        
        # Products table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(9)
        self.products_table.setHorizontalHeaderLabels([
            "SKU ID", "Barcode", "Category", "Subcategory", "Product Name",
            "Description", "Tax Rate", "Price", "Default Unit"
        ])
        self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.products_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.products_table.itemDoubleClicked.connect(self.load_product)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Product")
        self.save_button.clicked.connect(self.save_product)
        self.clear_button = QPushButton("Clear Form")
        self.clear_button.clicked.connect(self.clear_form)
        
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.clear_button)
        
        # Add all layouts to main layout
        layout.addLayout(details_layout)
        layout.addWidget(self.products_table)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)

    def get_db_connection(self):
        db_path = os.path.join('database', 'inventory.db')
        return sqlite3.connect(db_path)

    def load_categories(self):
        if not self.current_user:
            return
            
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        # Load categories
        cursor.execute("SELECT DISTINCT category FROM products WHERE user_id = ?", (self.current_user['id'],))
        categories = [row[0] for row in cursor.fetchall()]
        self.category_combo.clear()
        self.category_combo.addItems(categories)
        
        conn.close()

    def load_products(self):
        if not self.current_user:
            return
            
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT sku_id, barcode, category, subcategory, product_name,
                   description, tax_rate, price, default_unit
            FROM products
            WHERE user_id = ?
            ORDER BY product_name
        """, (self.current_user['id'],))
        
        products = cursor.fetchall()
        self.products_table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            for col, value in enumerate(product):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.products_table.setItem(row, col, item)
        
        conn.close()

    def browse_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Product Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_name:
            self.current_image_path = file_name
            pixmap = QPixmap(file_name)
            scaled_pixmap = pixmap.scaled(
                300, 300,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

    def clear_image(self):
        self.current_image_path = None
        self.image_label.clear()
        self.image_label.setStyleSheet("border: 1px solid #ccc;")

    def clear_form(self):
        self.barcode_input.clear()
        self.sku_input.clear()
        self.category_combo.setCurrentText("")
        self.subcategory_combo.setCurrentText("")
        self.name_input.clear()
        self.desc_input.clear()
        self.tax_input.clear()
        self.price_input.clear()
        self.unit_input.clear()
        self.clear_image()

    def save_product(self):
        if not self.current_user:
            QMessageBox.warning(self, "Error", "Please log in to save products")
            return
            
        # Get values from form
        sku_id = self.sku_input.text().strip()
        barcode = self.barcode_input.text().strip()
        category = self.category_combo.currentText().strip()
        subcategory = self.subcategory_combo.currentText().strip()
        product_name = self.name_input.text().strip()
        description = self.desc_input.toPlainText().strip()
        tax_rate = self.tax_input.text().strip()
        price = self.price_input.text().strip()
        default_unit = self.unit_input.text().strip()
        
        # Validate required fields
        if not all([sku_id, category, product_name, tax_rate, price, default_unit]):
            QMessageBox.warning(self, "Error", "Please fill in all required fields")
            return
        
        try:
            tax_rate = float(tax_rate)
            price = float(price)
        except ValueError:
            QMessageBox.warning(self, "Error", "Tax rate and price must be valid numbers")
            return
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Check if SKU ID already exists
            cursor.execute("SELECT id FROM products WHERE sku_id = ? AND user_id = ?", (sku_id, self.current_user['id']))
            if cursor.fetchone():
                QMessageBox.warning(self, "Error", "SKU ID already exists")
                return
            
            # Save image if exists
            image_path = None
            if self.current_image_path:
                # Create images directory if it doesn't exist
                os.makedirs('images', exist_ok=True)
                
                # Generate unique filename
                file_ext = os.path.splitext(self.current_image_path)[1]
                image_path = f"images/{sku_id}{file_ext}"
                
                # Copy image to images directory
                import shutil
                shutil.copy2(self.current_image_path, image_path)
            
            # Insert new product
            cursor.execute("""
                INSERT INTO products (
                    sku_id, barcode, category, subcategory, product_name,
                    description, tax_rate, price, default_unit, user_id, image_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sku_id, barcode, category, subcategory, product_name,
                description, tax_rate, price, default_unit, self.current_user['id'], image_path
            ))
            
            conn.commit()
            QMessageBox.information(self, "Success", "Product saved successfully")
            self.clear_form()
            self.load_products()
            self.load_categories()
            self.product_added.emit()  # Emit signal when product is added
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")
        finally:
            conn.close()

    def load_product(self, item):
        row = item.row()
        self.sku_input.setText(self.products_table.item(row, 0).text())
        self.barcode_input.setText(self.products_table.item(row, 1).text())
        self.category_combo.setCurrentText(self.products_table.item(row, 2).text())
        self.subcategory_combo.setCurrentText(self.products_table.item(row, 3).text())
        self.name_input.setText(self.products_table.item(row, 4).text())
        self.desc_input.setPlainText(self.products_table.item(row, 5).text())
        self.tax_input.setText(self.products_table.item(row, 6).text())
        self.price_input.setText(self.products_table.item(row, 7).text())
        self.unit_input.setText(self.products_table.item(row, 8).text()) 