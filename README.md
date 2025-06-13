# Flask Order Management System

A modern order management system built with Flask that handles basic order operations. It was developed as part of the technical task for the Galvan AI Backend Engineer Internship.

## Features

- Add new orders with details (items, sender, recipient, address, delivery date)
- Edit existing orders
- Delete orders
- Mark orders as delivered
- View all orders in a responsive HTML table
- Track order status (Pending, In Transit, Delivered)
- Log every action (create, edit, delete, mark delivered) with timestamp and actor
- Modern dark theme UI with responsive design

## Technical Stack

- **Backend**: Flask
- **Database**: SQLite
- **Templates**: Jinja2
- **Styling**: Custom CSS with modern dark theme
- **Icons**: Heroicons (SVG)

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/shahmeerahmed486/flask-order-system.git
cd flask-order-system
```

### 2. Create and activate virtual environment (optional but recommended)

```bash
python -m venv venv
```

**Windows:**  
```bash
venv\Scripts\activate
```

**macOS/Linux:**  
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Then open your browser and go to:  
`http://127.0.0.1:5000`

## Project Structure

```
Order-App/
├── app.py                 # Main Flask application
├── orders.db             # SQLite database
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── base.html        # Base template with common layout
│   ├── index.html       # Main page showing all orders
│   ├── add_order.html   # Form for adding new orders
│   ├── edit_order.html  # Form for editing orders
│   └── logs.html        # Page showing action logs
└── venv/                # Python virtual environment
```

## Implementation Details

- **Database**: Uses SQLite with two tables:
  - `orders`: Stores order information
  - `action_logs`: Tracks all actions performed on orders

- **Routes**:
  - `/`: View all orders
  - `/add_order`: Add a new order
  - `/edit_order/<id>`: Edit an existing order
  - `/delete_order/<id>`: Delete an order
  - `/mark_delivered/<id>`: Mark an order as delivered
  - `/logs`: View action logs

- **Features**:
  - Responsive design that works on mobile and desktop
  - Modern dark theme UI
  - Form validation
  - Confirmation dialogs for deletions
  - Flash messages for user feedback
  - Action logging with timestamps
  - Status management (Pending, In Transit, Delivered)

## Notes

- The virtual environment (`venv/`) is ignored from version control
- The database file (`orders.db`) is created automatically on first run
- No external UI libraries were used - all styling is custom CSS
- The application uses a single `app.py` file for simplicity
