import sqlite3

class VendingDatabase:
    """Handles vending machine database operations."""

    def __init__(self, db_name="vending_machine.db"):
        self.db_name = db_name

    def execute_query(self, query, params=(), fetch_one=True):
        try:
            print(f"Executing query: {query} with params: {params}")  # Debug print
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(query, params)  # Executes the update or query
            result = cursor.fetchone() if fetch_one else cursor.fetchall()
            conn.commit()
            conn.close()
            print(f"Query result: {result}")  # Debug print
            return result if result else []  # Return result directly if valid
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []


    # def get_item_price(self, item):
    #     """Returns the price of an item."""
    #     return self.execute_query("SELECT price FROM inventory WHERE item=?", (item))

    def check_stock(self, item):
        """Checks available stock."""
        return self.execute_query("SELECT stock FROM inventory WHERE item=?", (item))

    def update_stock(self, item):
        """Reduces stock by one for the selected item."""
        print(f"Updating stock for {item}")
        self.execute_query("UPDATE inventory SET stock = stock - 1 WHERE item=?", (item,), fetch_one=False)
        print(f"Stock update complete for {item}.")


    def get_all_items(self):
        """Fetches all items in the inventory (name, price, stock)."""
        result = self.execute_query("SELECT item, price, stock FROM inventory", fetch_one=False)
        print("Database query result:", result)  # Debug print
        return result if isinstance(result, list) else []


# Initialize database
def initialize_database():
    print("Initializing database...")
    conn = sqlite3.connect("vending_machine.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            item TEXT PRIMARY KEY,
            price INTEGER,
            stock INTEGER
        )
    ''')
    cursor.execute("DELETE FROM inventory")
    cursor.executemany("INSERT OR IGNORE INTO inventory VALUES (?, ?, ?)", [
        ('Gum', 15, 10),
        ('Apple', 20, 3),
        ('Yogurt', 25, 7),
        ('Chips', 30, 3),
        ('Soda', 50, 10)
    ])
    conn.commit()
    conn.close()
    print("Database initialized with items.")
