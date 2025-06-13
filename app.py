from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Database initialization
def init_db():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    
    # Create orders table
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number_of_items INTEGER NOT NULL,
            sender_name TEXT NOT NULL,
            recipient_name TEXT NOT NULL,
            recipient_address TEXT NOT NULL,
            delivery_date TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    
    # Create action_logs table
    c.execute('''
        CREATE TABLE IF NOT EXISTS action_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            order_id INTEGER,
            timestamp TEXT NOT NULL,
            actor TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

def log_action(action, order_id, actor):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO action_logs (action, order_id, timestamp, actor)
        VALUES (?, ?, ?, ?)
    ''', (action, order_id, datetime.now().isoformat(), actor))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('SELECT * FROM orders ORDER BY id DESC')
    orders = c.fetchall()
    conn.close()
    return render_template('index.html', orders=orders)

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO orders (number_of_items, sender_name, recipient_name, 
                              recipient_address, delivery_date, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            request.form['number_of_items'],
            request.form['sender_name'],
            request.form['recipient_name'],
            request.form['recipient_address'],
            request.form['delivery_date'],
            'Pending'
        ))
        
        order_id = c.lastrowid
        conn.commit()
        conn.close()
        
        log_action('create', order_id, 'System')
        flash('Order added successfully!')
        return redirect(url_for('index'))
    
    return render_template('add_order.html')

@app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        c.execute('''
            UPDATE orders 
            SET number_of_items = ?, sender_name = ?, recipient_name = ?,
                recipient_address = ?, delivery_date = ?, status = ?
            WHERE id = ?
        ''', (
            request.form['number_of_items'],
            request.form['sender_name'],
            request.form['recipient_name'],
            request.form['recipient_address'],
            request.form['delivery_date'],
            request.form['status'],
            order_id
        ))
        
        conn.commit()
        log_action('edit', order_id, 'System')
        flash('Order updated successfully!')
        return redirect(url_for('index'))
    
    c.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
    order = c.fetchone()
    conn.close()
    
    return render_template('edit_order.html', order=order)

@app.route('/delete_order/<int:order_id>')
def delete_order(order_id):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    conn.commit()
    conn.close()
    
    log_action('delete', order_id, 'System')
    flash('Order deleted successfully!')
    return redirect(url_for('index'))

@app.route('/mark_delivered/<int:order_id>')
def mark_delivered(order_id):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('UPDATE orders SET status = ? WHERE id = ?', ('Delivered', order_id))
    conn.commit()
    conn.close()
    
    log_action('mark_delivered', order_id, 'System')
    flash('Order marked as delivered!')
    return redirect(url_for('index'))

@app.route('/logs')
def view_logs():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('''
        SELECT action_logs.*, orders.id as order_id 
        FROM action_logs 
        LEFT JOIN orders ON action_logs.order_id = orders.id 
        ORDER BY timestamp DESC
    ''')
    logs = c.fetchall()
    conn.close()
    return render_template('logs.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True) 