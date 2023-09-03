import one
import pytest


class TestOne:
    def test_add(self):
        assert one.add(2, 3) == 5
        assert one.add(-2, 3) == 1

    def test_multiply(self):
        assert one.multiply(2, 3) == 6
        assert one.multiply(2, -3) == -6

    def test_division(self):
        assert one.division(10, 2) == 5
        with pytest.raises(ZeroDivisionError):
            one.division(5, 0)
    