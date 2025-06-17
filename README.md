# Inventory Management System

A desktop application built with Python and PySide6 for managing inventory, sales, and purchases.

## Features

- User Authentication (Sign Up/Login)
- Product Management
- Supplier Management
- Customer Management
- Goods Receiving
- Sales Management
- User-specific data isolation
- Automatic calculations for taxes and totals

## Requirements

- Python 3.8 or higher
- PySide6
- SQLite3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/inventory-manager.git
cd inventory-manager
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

## Default Admin Account

- Username: admin
- Password: admin123

## Project Structure

```
inventory-manager/
├── database/
│   └── db_setup.py
├── forms/
│   ├── customer_master.py
│   ├── goods_receiving.py
│   ├── product_master.py
│   ├── sales_form.py
│   ├── signup.py
│   └── supplier_master.py
├── images/
├── main.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 