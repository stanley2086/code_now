class coo():

    def __init__(self,name=None,year=None):
        self.name = name
        self.year = year

    @staticmethod
    def foo1(string):
        name,year = string.split(',')
        print('foo1_staticmethod:\nInfo: My name is: %s' %name, ', I was born in %s' %year)


    @classmethod
    def foo(cls,string):
        name,year = string.split(',')
        info = cls(name,year)
        return info

    def outdata(self):
        print('foo_classmethod:Info: ')
        print('My name is: %s' %self.name, ', I was born in %s' %self.year)

a = coo.foo('Jason,2010')
a.outdata()

b = coo.foo1('Mike,2012')

