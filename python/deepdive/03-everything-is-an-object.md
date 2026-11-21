# Everything is an object

Almost everything in python is a object (ie. an instance of a class)

For example `int` , `bool` , `float` , `str` are all objects of their respective class
Here, I am not talking about actual data.. I am talking about the types themselves..

YES! THAT'S RIGHT.. the types themselves are objects. To prove this, run below code:

```python

x = 10
print(type(x))

print(type(int))

```

You will get output like this:

> <class 'int'>
> <class 'type'>

Even more surprisingly other constructs like
- Functions (object of `function` class)
- Classes (object of `class` class)
etc are objects too..

```python

def say_hi(name):
    print(f"Hello, {name}")

print(type(say_hi))

class Test:
    def __init__(self):
        self.name = "Dummy data"

print(type(Test))

```

This leads to one important realization. Since these are all objects,
they have memory addresses...

YES, the functions that you define will get their own memory address.
as a consequence, we can assign a function to a variable,
as a consequence, functions can be passed to other functions just like a normal variable,
etc

