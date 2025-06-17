import sqlite3
import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QComboBox, QPushButton, QMessageBox,
                             QDoubleSpinBox, QTableWidget, QTableWidgetItem,
                             QSpinBox)
from PySide6.QtCore import Qt

class GoodsReceivingForm(QWidget):
    def __init__(self, product_master_form=None, current_user=None):
        super().__init__()
        self.product_master_form = product_master_form
        self.current_user = current_user
        self.setup_ui()
        self.load_products()
        self.load_suppliers()
        
        if product_master_form:
            product_master_form.product_added.connect(self.load_products)

    def get_db_connection(self):
        db_path = os.path.join('database', 'inventory.db')
        return sqlite3.connect(db_path)

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Form fields
        form_layout = QVBoxLayout()
        
        # Supplier
        supplier_layout = QHBoxLayout()
        supplier_label = QLabel("Supplier:")
        self.supplier_combo = QComboBox()
        self.supplier_combo.setEditable(True)
        supplier_layout.addWidget(supplier_label)
        supplier_layout.addWidget(self.supplier_combo)
        
        # Product
        product_layout = QHBoxLayout()
        product_label = QLabel("Product:")
        self.product_combo = QComboBox()
        product_layout.addWidget(product_label)
        product_layout.addWidget(self.product_combo)
        
        # Quantity
        quantity_layout = QHBoxLayout()
        quantity_label = QLabel("Quantity:")
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(1, 999999)
        quantity_layout.addWidget(quantity_label)
        quantity_layout.addWidget(self.quantity_input)
        
        # Rate
        rate_layout = QHBoxLayout()
        rate_label = QLabel("Rate:")
        self.rate_input = QDoubleSpinBox()
        self.rate_input.setRange(0, 999999.99)
        self.rate_input.setDecimals(2)
        rate_layout.addWidget(rate_label)
        rate_layout.addWidget(self.rate_input)
        
        # Tax Rate
        tax_layout = QHBoxLayout()
        tax_label = QLabel("Tax Rate (%):")
        self.tax_input = QDoubleSpinBox()
        self.tax_input.setRange(0, 100)
        self.tax_input.setDecimals(2)
        tax_layout.addWidget(tax_label)
        tax_layout.addWidget(self.tax_input)
        
        # Total Rate
        total_rate_layout = QHBoxLayout()
        total_rate_label = QLabel("Total Rate:")
        self.total_rate_label = QLabel("0.00")
        total_rate_layout.addWidget(total_rate_label)
        total_rate_layout.addWidget(self.total_rate_label)
        
        # Tax Amount
        tax_amount_layout = QHBoxLayout()
        tax_amount_label = QLabel("Tax Amount:")
        self.tax_amount_label = QLabel("0.00")
        tax_amount_layout.addWidget(tax_amount_label)
        tax_amount_layout.addWidget(self.tax_amount_label)
        
        # Total Amount
        total_amount_layout = QHBoxLayout()
        total_amount_label = QLabel("Total Amount:")
        self.total_amount_label = QLabel("0.00")
        total_amount_layout.addWidget(total_amount_label)
        total_amount_layout.addWidget(self.total_amount_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        clear_button = QPushButton("Clear Form")
        save_button.clicked.connect(self.save_receiving)
        clear_button.clicked.connect(self.clear_form)
        button_layout.addWidget(save_button)
        button_layout.addWidget(clear_button)
        
        # Add all layouts to form layout
        form_layout.addLayout(supplier_layout)
        form_layout.addLayout(product_layout)
        form_layout.addLayout(quantity_layout)
        form_layout.addLayout(rate_layout)
        form_layout.addLayout(tax_layout)
        form_layout.addLayout(total_rate_layout)
        form_layout.addLayout(tax_amount_layout)
        form_layout.addLayout(total_amount_layout)
        form_layout.addLayout(button_layout)
        
        # Receiving table
        self.receiving_table = QTableWidget()
        self.receiving_table.setColumnCount(8)
        self.receiving_table.setHorizontalHeaderLabels([
            "Supplier", "Product", "Quantity", "Rate", "Tax Rate",
            "Total Rate", "Tax Amount", "Total Amount"
        ])
        self.receiving_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.receiving_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.receiving_table.itemDoubleClicked.connect(self.load_receiving)
        
        # Add layouts to main layout
        layout.addLayout(form_layout)
        layout.addWidget(self.receiving_table)
        
        self.setLayout(layout)
        
        # Connect signals for automatic calculations
        self.quantity_input.valueChanged.connect(self.calculate_totals)
        self.rate_input.valueChanged.connect(self.calculate_totals)
        self.tax_input.valueChanged.connect(self.calculate_totals)
        self.product_combo.currentIndexChanged.connect(self.product_changed)

    def load_products(self):
        if not self.current_user:
            return
            
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT sku_id, product_name, tax_rate, price
            FROM products
            WHERE user_id = ?
            ORDER BY product_name
        """, (self.current_user['id'],))
        
        products = cursor.fetchall()
        self.product_combo.clear()
        
        for product in products:
            self.product_combo.addItem(f"{product[1]} ({product[0]})", {
                'sku_id': product[0],
                'tax_rate': product[2],
                'price': product[3]
            })
        
        conn.close()

    def load_suppliers(self):
        if not self.current_user:
            return
            
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name
            FROM suppliers
            WHERE user_id = ?
            ORDER BY name
        """, (self.current_user['id'],))
        
        suppliers = [row[0] for row in cursor.fetchall()]
        self.supplier_combo.clear()
        self.supplier_combo.addItems(suppliers)
        
        conn.close()

    def product_changed(self, index):
        if index >= 0:
            product_data = self.product_combo.itemData(index)
            if product_data:
                self.tax_input.setValue(product_data['tax_rate'])
                self.rate_input.setValue(product_data['price'])
                self.calculate_totals()

    def calculate_totals(self):
        quantity = self.quantity_input.value()
        rate = self.rate_input.value()
        tax_rate = self.tax_input.value()
        
        total_rate = quantity * rate
        tax_amount = total_rate * (tax_rate / 100)
        total_amount = total_rate + tax_amount
        
        self.total_rate_label.setText(f"{total_rate:.2f}")
        self.tax_amount_label.setText(f"{tax_amount:.2f}")
        self.total_amount_label.setText(f"{total_amount:.2f}")

    def save_receiving(self):
        if not self.current_user:
            QMessageBox.warning(self, "Error", "Please log in to save goods receiving")
            return
            
        # Get values from form
        supplier = self.supplier_combo.currentText().strip()
        product_index = self.product_combo.currentIndex()
        if product_index < 0:
            QMessageBox.warning(self, "Error", "Please select a product")
            return
            
        product_data = self.product_combo.itemData(product_index)
        quantity = self.quantity_input.value()
        rate = self.rate_input.value()
        tax_rate = self.tax_input.value()
        
        # Validate required fields
        if not supplier:
            QMessageBox.warning(self, "Error", "Please select a supplier")
            return
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Insert new receiving record
            cursor.execute("""
                INSERT INTO goods_receiving (
                    supplier, product_sku, quantity, rate, tax_rate,
                    total_rate, tax_amount, total_amount, user_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                supplier,
                product_data['sku_id'],
                quantity,
                rate,
                tax_rate,
                float(self.total_rate_label.text()),
                float(self.tax_amount_label.text()),
                float(self.total_amount_label.text()),
                self.current_user['id']
            ))
            
            conn.commit()
            QMessageBox.information(self, "Success", "Goods receiving saved successfully")
            self.clear_form()
            self.load_receiving_list()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")
        finally:
            conn.close()

    def clear_form(self):
        self.supplier_combo.setCurrentText("")
        self.product_combo.setCurrentIndex(-1)
        self.quantity_input.setValue(1)
        self.rate_input.setValue(0)
        self.tax_input.setValue(0)
        self.total_rate_label.setText("0.00")
        self.tax_amount_label.setText("0.00")
        self.total_amount_label.setText("0.00")

    def load_receiving_list(self):
        if not self.current_user:
            return
            
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT supplier, product_sku, quantity, rate, tax_rate,
                   total_rate, tax_amount, total_amount
            FROM goods_receiving
            WHERE user_id = ?
            ORDER BY id DESC
        """, (self.current_user['id'],))
        
        receiving_list = cursor.fetchall()
        self.receiving_table.setRowCount(len(receiving_list))
        
        for row, receiving in enumerate(receiving_list):
            for col, value in enumerate(receiving):
                item = QTableWidgetItem(str(value))
                self.receiving_table.setItem(row, col, item)
        
        conn.close()

    def load_receiving(self, item):
        row = item.row()
        supplier = self.receiving_table.item(row, 0).text()
        product_sku = self.receiving_table.item(row, 1).text()
        
        # Find supplier in combo box
        index = self.supplier_combo.findText(supplier)
        if index >= 0:
            self.supplier_combo.setCurrentIndex(index)
        
        # Find product in combo box
        for i in range(self.product_combo.count()):
            if self.product_combo.itemData(i)['sku_id'] == product_sku:
                self.product_combo.setCurrentIndex(i)
                break
        
        self.quantity_input.setValue(int(self.receiving_table.item(row, 2).text()))
        self.rate_input.setValue(float(self.receiving_table.item(row, 3).text()))
        self.tax_input.setValue(float(self.receiving_table.item(row, 4).text())) 