from fsm import VendingMachineFSM
from database import VendingDatabase,initialize_database
   
    
def run_vending_machine():
    initialize_database()
    db = VendingDatabase()  # Initialize the database
    fsm = VendingMachineFSM(db)

    while True:
        print("\nVending Machine - Main Menu")
        items = db.get_all_items()  # Display items
        for index, item in enumerate(items, start=1):
            if isinstance(item, tuple) and len(item) == 3:
                item_name, price, stock = item
                print(f"{index}. {item_name} - {price}¢ (Stock: {stock})")
            else:
                print("Error: Invalid item format.")

        item_index = int(input("\nSelect an item by number (or 0 to quit): "))
        if item_index == 0:
            print("Exiting vending machine...")
            break

        # Transition to item_selected state
        fsm.select_item(item_index)  # Trigger select_item event to transition

        # After selecting the item, the FSM should be in 'item_selected' state
        if fsm.state == 'item_selected':
            item_name, price, stock = fsm.selected_item  # Get the selected item details
            print(f"Item selected: {item_name} (Price: {price}¢)")

            # Now transition to money_inserted state
            while fsm.state == 'item_selected':  # Wait until money is inserted
                money_inserted = int(input("Insert money (in cents): "))
                fsm.insert_money(money_inserted)  # Add the inserted money to the FSM

            # Trigger check_sufficient_money to verify if the inserted money is sufficient
            fsm.check_sufficient_money()  # Check if enough money is inserted

            # If money is sufficient, dispense item and complete transaction
            if fsm.state == 'sufficient_money':
                fsm.dispense_item()  # Dispense the item

                choice = input("\nWould you like to shop more? (yes/no): ").strip().lower()
                if choice != "yes":
                    print("Thank you for using the vending machine. Goodbye!")
                    break
                
                fsm.complete_transaction()  # Complete the transaction

            # If money is insufficient, ask for additional money
            elif fsm.state == 'insufficient_money':
                remaining = fsm.selected_item[1] - fsm.money_inserted
                print(f"You still need {remaining}¢ to complete the purchase.")
                money_inserted = int(input(f"Insert additional {remaining}¢: "))
                fsm.insert_money(money_inserted)  # Add the additional inserted money
                fsm.check_sufficient_money()

                # Check again if money is now sufficient
                if fsm.state == 'sufficient_money':
                    fsm.dispense_item()  # Dispense the item
                    fsm.complete_transaction()  # Complete the transaction
                else:
                    print("Still insufficient money. Transaction failed.")
                    print("Returning inserted money")
                    fsm.go_idle()

        # Reset FSM after completing the transaction and return to idle state
        fsm.go_idle()

if __name__ == "__main__":
    run_vending_machine()

