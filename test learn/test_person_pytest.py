from person import Person
import pytest
import time


class TestPerson:
    @pytest.fixture
    def setup(self):   
        self.p1 = Person('Neda', 'razavi')
        self.p2 = Person('nazanin', 'Torabi')
        yield 'setup'
        time.sleep(2)
        
    def test_full_name(self, setup):
        assert self.p1.full_name() == 'neda razavi'
        assert self.p2.full_name() == 'nazanin torabi'

    def test_email(self, setup):
        assert self.p1.email() == 'nedarazavi@gmail.com'
        assert self.p2.email() == 'nazanintorabi@gmail.com'

