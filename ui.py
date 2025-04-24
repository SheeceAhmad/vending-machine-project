import tkinter as tk
from fsm import VendingMachine

def insert_money():
    vm.insert_money(25)

def select_item():
    vm.select_item("Apple")

def dispense_item():
    vm.dispense("Apple")

vm = VendingMachine()

root = tk.Tk()
root.title("Vending Machine")

tk.Button(root, text="Insert Money", command=insert_money).pack()
tk.Button(root, text="Select Item", command=select_item).pack()
tk.Button(root, text="Dispense", command=dispense_item).pack()

root.mainloop()
