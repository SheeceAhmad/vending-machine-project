import unittest
from fsm import VendingMachine

class TestFSM(unittest.TestCase):
    def setUp(self):
        self.vm = VendingMachine()

    def test_insert_money(self):
        self.vm.insert_money(25)
        self.assertEqual(self.vm.state, "Accepting Money")

    def test_invalid_selection(self):
        self.vm.insert_money(10)
        self.assertNotEqual(self.vm.select_item('Apple'), "Selecting Item")  # Not enough money

if __name__ == '__main__':
    unittest.main()
