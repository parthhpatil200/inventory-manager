# Application Theme Colors
PRIMARY_COLOR = "#2c3e50"  # Dark blue-gray
SECONDARY_COLOR = "#3498db"  # Bright blue
ACCENT_COLOR = "#e74c3c"  # Coral red
SUCCESS_COLOR = "#2ecc71"  # Emerald green
WARNING_COLOR = "#f1c40f"  # Yellow
BACKGROUND_COLOR = "#ecf0f1"  # Light gray
TEXT_COLOR = "#2c3e50"  # Dark blue-gray
WHITE = "#ffffff"

# Main Window Styles
MAIN_WINDOW_STYLE = f"""
QMainWindow {{
    background-color: {BACKGROUND_COLOR};
}}

QWidget {{
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}}

QPushButton {{
    background-color: {SECONDARY_COLOR};
    color: {WHITE};
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: #2980b9;
}}

QPushButton:pressed {{
    background-color: #2472a4;
}}

QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
    padding: 6px;
    border: 2px solid #bdc3c7;
    border-radius: 4px;
    background-color: {WHITE};
}}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 2px solid {SECONDARY_COLOR};
}}

QLabel {{
    color: {TEXT_COLOR};
    font-weight: bold;
}}

QTableWidget {{
    background-color: {WHITE};
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    gridline-color: #ecf0f1;
}}

QTableWidget::item {{
    padding: 5px;
}}

QTableWidget::item:selected {{
    background-color: {SECONDARY_COLOR};
    color: {WHITE};
}}

QHeaderView::section {{
    background-color: {PRIMARY_COLOR};
    color: {WHITE};
    padding: 8px;
    border: none;
    font-weight: bold;
}}

QComboBox::drop-down {{
    border: none;
}}

QComboBox::down-arrow {{
    image: url(resources/down_arrow.png);
    width: 12px;
    height: 12px;
}}

QMessageBox {{
    background-color: {WHITE};
}}

QMessageBox QPushButton {{
    min-width: 80px;
}}
"""

# Form-specific styles
FORM_STYLE = f"""
QWidget {{
    background-color: {WHITE};
    border-radius: 8px;
    padding: 16px;
}}

QGroupBox {{
    border: 2px solid {PRIMARY_COLOR};
    border-radius: 6px;
    margin-top: 12px;
    font-weight: bold;
    color: {PRIMARY_COLOR};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}}

QPushButton {{
    background-color: {PRIMARY_COLOR};
    color: {WHITE};
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 11pt;
    min-width: 120px;
}}

QPushButton:hover {{
    background-color: #34495e;
}}

QPushButton:pressed {{
    background-color: #2c3e50;
}}

QPushButton[text="Clear Form"], QPushButton[text="Clear Filters"] {{
    background-color: #e74c3c;
}}

QPushButton[text="Clear Form"]:hover, QPushButton[text="Clear Filters"]:hover {{
    background-color: #c0392b;
}}

QPushButton[text="Clear Form"]:pressed, QPushButton[text="Clear Filters"]:pressed {{
    background-color: #a93226;
}}

QComboBox {{
    border: 2px solid {PRIMARY_COLOR};
    border-radius: 4px;
    padding: 5px 30px 5px 10px;
    background-color: white;
    min-height: 30px;
}}

QComboBox:hover {{
    border-color: #34495e;
}}

QComboBox:focus {{
    border-color: #2980b9;
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
    background-color: {PRIMARY_COLOR};
    border-top-right-radius: 2px;
    border-bottom-right-radius: 2px;
}}

QComboBox::down-arrow {{
    image: url(resources/down_arrow.png);
    width: 16px;
    height: 16px;
}}

QComboBox QAbstractItemView {{
    border: 2px solid {PRIMARY_COLOR};
    border-radius: 4px;
    background-color: white;
    selection-background-color: {PRIMARY_COLOR};
    selection-color: white;
}}
"""

# Navigation button styles
NAV_BUTTON_STYLE = f"""
QPushButton {{
    background-color: {PRIMARY_COLOR};
    color: {WHITE};
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 11pt;
    min-width: 120px;
}}

QPushButton:hover {{
    background-color: #34495e;
}}

QPushButton:pressed {{
    background-color: #2c3e50;
}}
""" 