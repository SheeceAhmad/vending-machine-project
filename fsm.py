from transitions import Machine

class VendingMachineFSM:
    def __init__(self, db):
        self.db = db
        self.selected_item = None
        self.money_inserted = 0
        self.state = "idle"  # Set initial state as "idle"
        self.machine = Machine(model=self, states=["idle", "item_selected", "money_inserted", "sufficient_money", "insufficient_money"], initial="idle")

        # Define transitions
        self.machine.add_transition(trigger="select_item", source="idle", dest="item_selected", after="item_selected_state")
        self.machine.add_transition(trigger="insert_money", source="item_selected", dest="money_inserted", before="insert_money_state")
        self.machine.add_transition(trigger="insert_money", source="insufficient_money", dest="money_inserted", before="insert_money_state")
        self.machine.add_transition(trigger="check_sufficient_money", source="money_inserted", dest="sufficient_money", conditions="is_sufficient_money")
        self.machine.add_transition(trigger="check_sufficient_money", source="money_inserted", dest="insufficient_money", conditions="is_insufficient_money")

    def item_selected_state(self, item_index):
        items = self.db.get_all_items()
        item_name, price, stock = items[item_index - 1]

        # Check if stock is available
        if stock <= 0:
            print(f"Sorry, {item_name} is out of stock!")
            self.state = 'idle'  # Reset state to idle if out of stock
            return
        
        self.selected_item = (item_name, price, stock)
        print(f"Item selected: {item_name} (Price: {price}¢)")

    def insert_money_state(self, amount):
        self.money_inserted += amount
        print(f"Money inserted: {self.money_inserted}¢. Total price: {self.selected_item[1]}¢.")

    def is_sufficient_money(self):
        return self.money_inserted >= self.selected_item[1]

    def is_insufficient_money(self):
        return self.money_inserted < self.selected_item[1]

    def dispense_item(self):
        if self.selected_item:
            item_name, price, stock = self.selected_item
            print(f"Dispensing {item_name}. Change: {self.money_inserted - price}¢.")
            # Update stock only once here after the item is dispensed
            self.db.update_stock(item_name)
            self.complete_transaction()
        

    def complete_transaction(self, event_data=None):
        # Finalize the transaction, regardless of the outcome
        print(f"Transaction completed. Dispensing item.")
        self.go_idle()

    def go_idle(self):
        self.money_inserted = 0
        self.selected_item = None
        self.state = "idle"
