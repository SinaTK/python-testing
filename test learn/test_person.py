import unittest
from person import Person


class TestPerson(unittest.TestCase):
    def setUp(self):   
        self.p1 = Person('Neda', 'razavi')
        self.p2 = Person('nazanin', 'Torabi')

    def tearDown(self):
        print('Test is done...')

    def test_full_name(self):
        self.assertEqual(self.p1.full_name(), 'neda razavi')
        self.assertEqual(self.p2.full_name(), 'nazanin torabi')

    def test_email(self):
        self.assertEqual(self.p1.email(), 'nedarazavi@gmail.com')
        self.assertEqual(self.p2.email(), 'nazanintorabi@gmail.com')

if __name__ == '__main__':
    unittest.main()
