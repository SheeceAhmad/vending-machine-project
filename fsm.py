from transitions import Machine
from database import VendingDatabase

class VendingMachine:
    states = ['Idle', 'Accepting Money', 'Selecting Item', 'Dispensing', 'Error']

    def __init__(self):
        self.machine = Machine(model=self, states=self.states, initial='Idle')
        self.balance = 0
        self.db = VendingDatabase()  # Initialize database connection

        # Define transitions
        self.machine.add_transition('insert_money', 'Idle', 'Accepting Money', after='add_money')
        self.machine.add_transition('select_item', 'Accepting Money', 'Selecting Item', conditions=['valid_selection'])
        self.machine.add_transition('dispense', 'Selecting Item', 'Dispensing', conditions=['can_dispense'], after='complete_transaction')
        self.machine.add_transition('reset', '*', 'Idle')
        self.machine.add_transition('error', '*', 'Error')

    def add_money(self, amount):
        """Add money and update balance."""
        self.balance += amount
        print(f"Balance: {self.balance} cents")

    def valid_selection(self, item):
        """Check if the selected item is available and the balance is sufficient."""
        price = self.db.get_item_price(item)
        if price is None:
            print(f"Error: {item} is not available.")
            return False
        return self.balance >= price

    def can_dispense(self, item):
        """Ensure item is in stock before dispensing."""
        stock = self.db.check_stock(item)
        return stock > 0

    def complete_transaction(self, item):
        """Deduct balance, update inventory, and finalize purchase."""
        price = self.db.get_item_price(item)
        self.balance -= price
        self.db.update_stock(item)
        print(f"Dispensing {item}. Remaining Balance: {self.balance} cents.")
