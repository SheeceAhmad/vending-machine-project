import tkinter as tk
from fsm import VendingMachine
from database import VendingDatabase  # Ensure this path matches your file

# Initialize vending machine and database
vm = VendingMachine()
db = VendingDatabase()  # Initialize database connection

# Function to fetch all available items from the database and show them in the GUI
def get_available_items():
    items = db.get_all_items()  # Get all items from the inventory
    return items

# GUI Logic Functions
def select_item(item):
    vm.select_item(item)
    update_status()

def insert(amount):
    vm.insert_money(amount)
    update_status()

def dispense_item():
    vm.dispense()
    update_status()

def reset_machine():
    vm.reset_machine()
    update_status()

def update_status():
    """Update the status label with current machine state and balance"""
    state = vm.state
    balance = vm.balance
    selected_item = vm.selected_item if hasattr(vm, 'selected_item') else 'None'
    status_label.config(text=f"State: {state} | Balance: {balance}¢ | Selected Item: {selected_item}")

# Build GUI
root = tk.Tk()
root.title("Vending Machine")

# Title Label
tk.Label(root, text="Vending Machine UI", font=("Arial", 14)).pack(pady=10)

# Insert money buttons
tk.Button(root, text="Insert 5¢", width=20, command=lambda: insert(5)).pack(pady=2)
tk.Button(root, text="Insert 10¢", width=20, command=lambda: insert(10)).pack(pady=2)
tk.Button(root, text="Insert 25¢", width=20, command=lambda: insert(25)).pack(pady=2)

# Dynamically create buttons for each available item
items = get_available_items()
for item, price, stock in items:
    tk.Button(root, text=f"Select {item} - {price}¢", width=20, command=lambda item=item: select_item(item)).pack(pady=5)

# Dispense and Reset Buttons
tk.Button(root, text="Dispense", width=20, command=dispense_item).pack(pady=2)
tk.Button(root, text="Reset", width=20, command=reset_machine).pack(pady=5)

# Status label
status_label = tk.Label(root, text="State: Idle | Balance: 0¢ | Selected Item: None", font=("Arial", 10))
status_label.pack(pady=10)

# Run the GUI
root.mainloop()
