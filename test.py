'''
Created on 26. sep. 2016

@author: MartinHuusBjerge
'''

class Singleton(type):
    _instances = {}
    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]

#Python3
class MyClass(metaclass=Singleton):
    
    def __init__(self):
        self.a = 1
        
    def afun(self):
        print('this is s function')


if __name__ == '__main__':
    a = 1028
    offset = 10
    print(a & (1 << offset))
