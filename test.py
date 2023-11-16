a={'a':1}
b={'b':{
    'c':2
}}
b.__delitem__('b')
print(b)