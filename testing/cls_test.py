
class TestClass(object):
    a = None

    def __init__(self):
        self.a = "hej"

    def sayHi(self):
        print "Hi", self.a, "!"

    def create(cls):
        o = cls()
        o.a = "no"
        return o

    create = classmethod(create)


a = TestClass()
print a
a.sayHi()

b = TestClass.create()
print b
b.sayHi()
