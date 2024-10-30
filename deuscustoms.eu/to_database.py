import csv
import sqlite3

# Connect to SQLite database (or create it)
conn = sqlite3.connect('deus_customs_products.db')
cursor = conn.cursor()

# Create a table for product data
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    link TEXT,
    title TEXT,
    price TEXT,
    description TEXT
)
''')

# Read the CSV file and insert data into the table
with open('deus_product_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute('''
        INSERT INTO products (link, title, price, description)
        VALUES (?, ?, ?, ?)
        ''', (row['Link'], row['Title'], row['Price'], row['Description']))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data has been stored in the database successfully.")
