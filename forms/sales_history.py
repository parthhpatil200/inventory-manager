import sqlite3
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QComboBox, QPushButton, QMessageBox,
                             QTableWidget, QTableWidgetItem, QScrollArea,
                             QGroupBox)
from PySide6.QtCore import Qt
from styles import FORM_STYLE

class SalesHistoryForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_sales_history()
        self.setStyleSheet(FORM_STYLE)

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
        
        # Search filters
        filter_group = QGroupBox("Search Filters")
        filter_layout = QVBoxLayout()
        filter_layout.setSpacing(15)
        
        # Date range
        date_layout = QHBoxLayout()
        from_date_label = QLabel("From Date:")
        self.from_date_input = QLineEdit()
        self.from_date_input.setPlaceholderText("YYYY-MM-DD")
        self.from_date_input.setMinimumHeight(30)
        to_date_label = QLabel("To Date:")
        self.to_date_input = QLineEdit()
        self.to_date_input.setPlaceholderText("YYYY-MM-DD")
        self.to_date_input.setMinimumHeight(30)
        date_layout.addWidget(from_date_label)
        date_layout.addWidget(self.from_date_input)
        date_layout.addWidget(to_date_label)
        date_layout.addWidget(self.to_date_input)
        
        # Product filter
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
        
        # Customer filter
        customer_layout = QHBoxLayout()
        customer_label = QLabel("Customer:")
        self.customer_combo = QComboBox()
        self.customer_combo.setPlaceholderText("Select customer")
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
        
        # Add layouts to filter group
        filter_layout.addLayout(date_layout)
        filter_layout.addLayout(product_layout)
        filter_layout.addLayout(customer_layout)
        filter_group.setLayout(filter_layout)
        
        # Sales history table
        table_group = QGroupBox("Sales History")
        table_layout = QVBoxLayout()
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(8)
        self.sales_table.setHorizontalHeaderLabels([
            "Date", "Customer", "Product", "Quantity", "Rate",
            "Tax Rate", "Tax Amount", "Total Amount"
        ])
        self.sales_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.sales_table.setEditTriggers(QTableWidget.NoEditTriggers)
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
        self.search_button = QPushButton("Search")
        self.clear_button = QPushButton("Clear Filters")
        self.search_button.setMinimumHeight(40)
        self.clear_button.setMinimumHeight(40)
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.clear_button)
        
        # Add all layouts to main layout
        layout.addWidget(filter_group)
        layout.addWidget(table_group)
        layout.addLayout(button_layout)
        
        main_widget.setLayout(layout)
        scroll.setWidget(main_widget)
        
        # Create outer layout for scroll area
        outer_layout = QVBoxLayout()
        outer_layout.addWidget(scroll)
        self.setLayout(outer_layout)
        
        # Connect signals
        self.search_button.clicked.connect(self.search_sales)
        self.clear_button.clicked.connect(self.clear_filters)

    def load_sales_history(self):
        # Implementation of load_sales_history method
        pass

    def search_sales(self):
        # Implementation of search_sales method
        pass

    def clear_filters(self):
        # Implementation of clear_filters method
        pass

    def search_sales(self):
        # Implementation of search_sales method
        pass

    def clear_filters(self):
        # Implementation of clear_filters method
        pass 