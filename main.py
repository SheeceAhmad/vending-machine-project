from fsm import VendingMachine

vm = VendingMachine()

vm.insert_money(20)  # Insert money
vm.select_item('Apple')  # Select Apple
vm.dispense('Apple')  # Dispensing Apple
