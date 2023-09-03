import one

def test_add():
    assert one.add(2, 3) == 5
    assert one.add(-2, 3) == 1

def test_multiply():
    assert one.multiply(2, 3) == 6
    assert one.multiply(2, -3) == -6

def test_division():
    assert one.division(10, 2) == 5
    