def add(x, y):
    return x + y


def multiply(x, y):
    return x * y

def division(x, y):
    if y == 0:
        raise ZeroDivisionError("Can't divide to zero")
    return x / y