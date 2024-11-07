from pprint import pprint
class POC:
    name: str
    contact: int

    def __init__(self, name, contact):
        self.name = name
        self.contact = contact

p1 = POC('John Doe', 1234567890)
pprint(p1.__dict__)