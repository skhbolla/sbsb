# *args

Recall the following with iterable unpacking (specifically tuple unpacking)

```python

a, b, *c = 10, 20, 'a', 'b'

```

In above code, the RHS is a tuple which gets unpacked into the LSS variables. So, a = 10 , b = 20 and c = ['a', 'b']

NOTE very important that c is a **list** of the packed values. This is the default behavior of `*` .. it collects the remaining values into a **list**


## *args in a function

Following the same logic as above, we can write code like this

```python

def func1(a, b, *c):
    #code
    pass

func1(10, 20, 'a', 'b')

```

WARN the value of c now **NOT BE A LIST** , it will be a *TUPLE*
ie a = 10 , b = 20 ; but c = ('a', 'b')

WARN also note that *args exhausts positional arguments, so we cannot add more parameters after it.
