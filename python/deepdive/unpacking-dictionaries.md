# The `**` unpacking operator

Consider the below piece of code

```python

d1 = {'key1': 1, 'key2': 2}
d2 = {'key3': 3, 'key4': 4}

l = [*d1, *d2]

```

What is the result of `l`?

Well, l will contain only the **keys** from the dictionaries.

Now, what if we want to unpack both keys and values from dictionaries..
Python provides the `**` operator for just this...

One very important thing to note here is that, unlike the `*` operator which can
be used in both LHS and RHS; the `**` operator can only be used on the RHS.

```python

d1 = {'k1': 1, 'k2': 2}
d2 = {'k3': 3, 'k4': 4}
d3 = {'k4': 0, 'k5': 5}

d  = {**d1, **d2, **d3}  # {'k1':1, 'k2':2, 'k3':3, 'k4':0, 'k5':5}


# Pay special attention to what happened to the key 'k4'
# Since a dictionary cannot have duplicate keys, the k4 key from d3 overrides 
# the k4 key from d2. Hence the output.

```
