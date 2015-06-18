import os
import pickle


PATH = "data/"

SENTINEL = object()
class MagicAttribute(object):
    def __init__(self, name, keyattr="name"):
        self.keyattr = keyattr
        self.name = name
        
    def get_filename(self, instance):
        return "{}{}_{}.dat".format(
            PATH, 
            instance.__class__.__name__, 
            getattr(instance, self.keyattr)
        )
    def load(self, instance):
        try:
            instance._data = pickle.load(open(self.get_filename(instance), "rb"))
        except (IOError, EOFError):
            instance._data = {}
    
    def write(self, instance):
        with open(self.get_filename(instance), "wb") as data_file:
            pickle.dump(instance._data, data_file, 2)

    def __get__(self, instance, owner):
        if not hasattr(instance, "_data"):
            self.load(instance)
        try:
            return instance._data[self.name]
        except KeyError:
            raise AttributeError
    
    def __set__(self, instance, value):
        if not hasattr(instance, "_data"):
            self.load(instance)
        prev_value = instance._data.get(self.name, SENTINEL)
        if value == prev_value:
            return
        instance._data[self.name] = value
        self.write(instance)

class MagicPerson(object):
    age = MagicAttribute("age")
    address = MagicAttribute("address")
    def __init__(self, name, age=None, address=None):
        self.name = name
        if age is not None:
            self.age = age
        if address  is not None:
            self.address = address
            
    

__doc__ = """
>>> from magicperson import MagicPerson
>>> 
>>> a = MagicPerson("Daniel")
>>> a.age = 8
>>> a.address = "Campinas"
>>> 
>>> b = MagicPerson("Daniel")
>>> b.age
8
>>> b.address
'Campinas'
>>> 
"""
