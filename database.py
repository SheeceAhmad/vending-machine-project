import sqlite3

class VendingDatabase:
    """Handles vending machine database operations."""
    
    def __init__(self, db_name="vending_machine.db"):
        self.db_name = db_name

    def execute_query(self, query, params=(), fetch_one=True):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone() if fetch_one else cursor.fetchall()
        conn.commit()
        conn.close()
        return result[0] if result else None

    def get_item_price(self, item):
        """Returns the price of an item."""
        return self.execute_query("SELECT price FROM inventory WHERE item=?", (item,))

    def check_stock(self, item):
        """Checks available stock."""
        return self.execute_query("SELECT stock FROM inventory WHERE item=?", (item,))

    def update_stock(self, item):
        """Reduces stock by one."""
        self.execute_query("UPDATE inventory SET stock = stock - 1 WHERE item=?", (item,), fetch_one=False)

# Initialize database
def initialize_database():
    conn = sqlite3.connect("vending_machine.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            item TEXT PRIMARY KEY,
            price INTEGER,
            stock INTEGER
        )
    ''')
    cursor.executemany("INSERT OR IGNORE INTO inventory VALUES (?, ?, ?)", [
        ('Gum', 15, 10),
        ('Apple', 20, 5),
        ('Yogurt', 25, 7)
    ])
    conn.commit()
    conn.close()

initialize_database()
