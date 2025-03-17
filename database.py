import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Change if necessary
            password="1602",  # Change if necessary
            database="BillingDB"
        )
        self.cursor = self.conn.cursor()

    def add_customer(self, name, phone):
        try:
            self.cursor.execute("INSERT INTO customers (name, phone) VALUES (%s, %s)", (name, phone))
            self.conn.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            print("Error:", err)

    def add_bill(self, customer_id, amount):
        self.cursor.execute("INSERT INTO bills (customer_id, amount) VALUES (%s, %s)", (customer_id, amount))
        self.conn.commit()

    def get_customers(self):
        self.cursor.execute("SELECT * FROM customers")
        return self.cursor.fetchall()

    def get_bills(self):
        self.cursor.execute("""
            SELECT bills.id, customers.name, bills.amount, bills.date 
            FROM bills 
            JOIN customers ON bills.customer_id = customers.id
        """)
        return self.cursor.fetchall()

    def update_customer(self, customer_id, name, phone):
        self.cursor.execute("UPDATE customers SET name=%s, phone=%s WHERE id=%s", (name, phone, customer_id))
        self.conn.commit()

    def delete_customer(self, customer_id):
        self.cursor.execute("DELETE FROM customers WHERE id=%s", (customer_id,))
        self.conn.commit()

    def update_bill(self, bill_id, amount):
        self.cursor.execute("UPDATE bills SET amount=%s WHERE id=%s", (amount, bill_id))
        self.conn.commit()

    def delete_bill(self, bill_id):
        self.cursor.execute("DELETE FROM bills WHERE id=%s", (bill_id,))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
