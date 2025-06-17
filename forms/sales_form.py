import sqlite3
import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QComboBox, QPushButton, QMessageBox,
                             QDoubleSpinBox, QTableWidget, QTableWidgetItem,
                             QSpinBox, QScrollArea, QGroupBox)
from PySide6.QtCore import Qt
from styles import FORM_STYLE

class SalesForm(QWidget):
    def __init__(self, product_master_form=None, current_user=None):
        super().__init__()
        self.product_master_form = product_master_form
        self.current_user = current_user
        self.setup_ui()
        self.load_products()
        self.load_customers()
        self.load_sales_list()
        self.setStyleSheet(FORM_STYLE)
        
        if product_master_form:
            product_master_form.product_added.connect(self.load_products)

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
        form_group = QGroupBox("Sales Details")
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Customer
        customer_layout = QHBoxLayout()
        customer_label = QLabel("Customer:")
        self.customer_combo = QComboBox()
        self.customer_combo.setEditable(True)
        self.customer_combo.setPlaceholderText("Select or enter customer")
        self.customer_combo.setMinimumHeight(30)
        self.customer_combo.setStyleSheet("""
            QComboBox {
                padding-right: 20px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(resources/down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        customer_layout.addWidget(customer_label)
        customer_layout.addWidget(self.customer_combo)
        
        # Product
        product_layout = QHBoxLayout()
        product_label = QLabel("Product:")
        self.product_combo = QComboBox()
        self.product_combo.setPlaceholderText("Select product")
        self.product_combo.setMinimumHeight(30)
        self.product_combo.setStyleSheet("""
            QComboBox {
                padding-right: 20px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(resources/down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        product_layout.addWidget(product_label)
        product_layout.addWidget(self.product_combo)
        
        # Quantity
        quantity_layout = QHBoxLayout()
        quantity_label = QLabel("Quantity:")
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(1, 999999)
        self.quantity_input.setMinimumHeight(30)
        quantity_layout.addWidget(quantity_label)
        quantity_layout.addWidget(self.quantity_input)
        
        # Rate
        rate_layout = QHBoxLayout()
        rate_label = QLabel("Rate:")
        self.rate_input = QDoubleSpinBox()
        self.rate_input.setRange(0, 999999.99)
        self.rate_input.setDecimals(2)
        self.rate_input.setMinimumHeight(30)
        rate_layout.addWidget(rate_label)
        rate_layout.addWidget(self.rate_input)
        
        # Tax Rate
        tax_layout = QHBoxLayout()
        tax_label = QLabel("Tax Rate (%):")
        self.tax_input = QDoubleSpinBox()
        self.tax_input.setRange(0, 100)
        self.tax_input.setDecimals(2)
        self.tax_input.setMinimumHeight(30)
        tax_layout.addWidget(tax_label)
        tax_layout.addWidget(self.tax_input)
        
        # Total Rate
        total_rate_layout = QHBoxLayout()
        total_rate_label = QLabel("Total Rate:")
        self.total_rate_label = QLabel("0.00")
        self.total_rate_label.setMinimumHeight(30)
        total_rate_layout.addWidget(total_rate_label)
        total_rate_layout.addWidget(self.total_rate_label)
        
        # Tax Amount
        tax_amount_layout = QHBoxLayout()
        tax_amount_label = QLabel("Tax Amount:")
        self.tax_amount_label = QLabel("0.00")
        self.tax_amount_label.setMinimumHeight(30)
        tax_amount_layout.addWidget(tax_amount_label)
        tax_amount_layout.addWidget(self.tax_amount_label)
        
        # Total Amount
        total_amount_layout = QHBoxLayout()
        total_amount_label = QLabel("Total Amount:")
        self.total_amount_label = QLabel("0.00")
        self.total_amount_label.setMinimumHeight(30)
        total_amount_layout.addWidget(total_amount_label)
        total_amount_layout.addWidget(self.total_amount_label)
        
        # Add all layouts to form layout
        form_layout.addLayout(customer_layout)
        form_layout.addLayout(product_layout)
        form_layout.addLayout(quantity_layout)
        form_layout.addLayout(rate_layout)
        form_layout.addLayout(tax_layout)
        form_layout.addLayout(total_rate_layout)
        form_layout.addLayout(tax_amount_layout)
        form_layout.addLayout(total_amount_layout)
        
        form_group.setLayout(form_layout)
        
        # Sales table
        table_group = QGroupBox("Sales History")
        table_layout = QVBoxLayout()
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(8)
        self.sales_table.setHorizontalHeaderLabels([
            "Customer", "Product", "Quantity", "Rate", "Tax Rate",
            "Total Rate", "Tax Amount", "Total Amount"
        ])
        self.sales_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.sales_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.sales_table.itemDoubleClicked.connect(self.load_sale)
        self.sales_table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
            }
        """)
        table_layout.addWidget(self.sales_table)
        table_group.setLayout(table_layout)
        
        # Action buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Sale")
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
        
        # Connect signals for automatic calculations
        self.quantity_input.valueChanged.connect(self.calculate_totals)
        self.rate_input.valueChanged.connect(self.calculate_totals)
        self.tax_input.valueChanged.connect(self.calculate_totals)
        self.product_combo.currentIndexChanged.connect(self.product_changed)
        self.save_button.clicked.connect(self.save_sale)
        self.clear_button.clicked.connect(self.clear_form)

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

    def load_customers(self):
        if not self.current_user:
            return
            
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name
            FROM customers
            WHERE user_id = ?
            ORDER BY name
        """, (self.current_user['id'],))
        
        customers = [row[0] for row in cursor.fetchall()]
        self.customer_combo.clear()
        self.customer_combo.addItems(customers)
        
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

    def save_sale(self):
        if not self.current_user:
            QMessageBox.warning(self, "Error", "Please log in to save sales")
            return
            
        # Get values from form
        customer = self.customer_combo.currentText().strip()
        product_index = self.product_combo.currentIndex()
        if product_index < 0:
            QMessageBox.warning(self, "Error", "Please select a product")
            return
            
        product_data = self.product_combo.itemData(product_index)
        quantity = self.quantity_input.value()
        rate = self.rate_input.value()
        tax_rate = self.tax_input.value()
        
        # Validate required fields
        if not customer:
            QMessageBox.warning(self, "Error", "Please select a customer")
            return
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Insert new sale record
            cursor.execute("""
                INSERT INTO sales (
                    customer, product_sku, quantity, rate, tax_rate,
                    total_rate, tax_amount, total_amount, user_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                customer,
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
            QMessageBox.information(self, "Success", "Sale saved successfully")
            self.clear_form()
            self.load_sales_list()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {str(e)}")
        finally:
            conn.close()

    def clear_form(self):
        self.customer_combo.setCurrentText("")
        self.product_combo.setCurrentIndex(-1)
        self.quantity_input.setValue(1)
        self.rate_input.setValue(0)
        self.tax_input.setValue(0)
        self.total_rate_label.setText("0.00")
        self.tax_amount_label.setText("0.00")
        self.total_amount_label.setText("0.00")

    def load_sales_list(self):
        if not self.current_user:
            return
            
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        # Join with products table to get product names
        cursor.execute("""
            SELECT s.customer, p.product_name, s.quantity, s.rate, s.tax_rate,
                   s.total_rate, s.tax_amount, s.total_amount
            FROM sales s
            LEFT JOIN products p ON s.product_sku = p.sku_id AND s.user_id = p.user_id
            WHERE s.user_id = ?
            ORDER BY s.id DESC
        """, (self.current_user['id'],))
        
        sales = cursor.fetchall()
        self.sales_table.setRowCount(len(sales))
        
        for row, sale in enumerate(sales):
            for col, value in enumerate(sale):
                # Format numeric values to 2 decimal places
                if isinstance(value, (int, float)):
                    display_value = f"{value:.2f}"
                else:
                    display_value = str(value) if value is not None else ""
                item = QTableWidgetItem(display_value)
                self.sales_table.setItem(row, col, item)
        
        # Resize columns to content
        self.sales_table.resizeColumnsToContents()
        
        conn.close()

    def load_sale(self, item):
        row = item.row()
        customer = self.sales_table.item(row, 0).text()
        product_sku = self.sales_table.item(row, 1).text()
        
        # Find customer in combo box
        index = self.customer_combo.findText(customer)
        if index >= 0:
            self.customer_combo.setCurrentIndex(index)
        
        # Find product in combo box
        for i in range(self.product_combo.count()):
            if self.product_combo.itemData(i)['sku_id'] == product_sku:
                self.product_combo.setCurrentIndex(i)
                break
        
        self.quantity_input.setValue(int(self.sales_table.item(row, 2).text()))
        self.rate_input.setValue(float(self.sales_table.item(row, 3).text()))
        self.tax_input.setValue(float(self.sales_table.item(row, 4).text())) 