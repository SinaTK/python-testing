class Person:
    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname

    def full_name(self):
        return '{} {}'.format(self.fname.lower(), self.lname.lower())
    
    def email(self):
        return '{}@gmail.com'.format(self.full_name()).replace(' ', '')
    

# p1 = Person('Neda', 'noori')
# print(p1.full_name())
# print(p1.email())