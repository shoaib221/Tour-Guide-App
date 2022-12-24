import os
import django
from django import forms
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bravo1.settings")
django.setup()


def Fly(*args, **kwargs):
    dic = kwargs.get('initial', None) # get the value of key@initial from key word arguments(**kwargs), which is a dictionary(dic)
    print(dic)
    var = dic.get('a', None) # get the value of key@a  from the dictionary(dic) which is a string('A')
    print(var)

    for keys in kwargs: # kwargs is a dictionary <class 'dict'>
        print(keys, kwargs.get(keys,None) )
        values = kwargs.get(keys, None)
        for k1 in values: # iterating dictionary
            print(k1,values.get(k1, None))

    for item in args: # iterating positional arguments (*args)
        print(item)


Fly('My Book', 'is New', initial={'a': 'A', 'b': 'B'}, upto = {'x': 'X', 'y': 'Y'})

'''
{'a': 'A', 'b': 'B'}
A
initial {'a': 'A', 'b': 'B'}
a A
b B
upto {'x': 'X', 'y': 'Y'}
x X
y Y
My Book
is New
'''
