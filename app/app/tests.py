from django.test import SimpleTestCase
from app import calc

class CalcTests(SimpleTestCase):
    "Test the calc module."
    #method       #method so you need self
    def test_add_numbers(self):
        "adding nums together"
        res = calc.add(5, 6)
        self.assertEqual(res, 11)

    def test_sub_numbers(self):
        res = calc.sub(10, 8)
        self.assertEqual(res, 2)
