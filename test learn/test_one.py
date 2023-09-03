import unittest
import one

class TestOne(unittest.TestCase):
    def test_add(self):
        self.assertEqual(one.add(2, 3), 5)
        self.assertEqual(one.add(2, -2), 0)
    
    def test_multiply(self):
        self.assertEqual(one.multiply(2, 5), 10)
        self.assertEqual(one.multiply(2, -5), -10)
        self.assertEqual(one.multiply(-2, -5), 10)

    def test_division(self):
        self.assertEqual(one.division(10, 2), 5)
        self.assertRaises(ZeroDivisionError, one.division, 2, 0)


if __name__ == '__main__':
    unittest.main()    
