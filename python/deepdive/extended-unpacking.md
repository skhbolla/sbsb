# Extended Unpacking

We dont always want to unpack every single item in an iterable.
We may, for example, want to unpack the first value into one variable,
and unpack the rest into another variable.

How could we do this?

```python

l = [1,2,3,4,5]
x, y = l[0], l[1:]

```

In above code, we leveraged the fact that lists are sequence iterables
i.e they have indexing and supports slicing.

But not all iterables are sequences... How do we deal with this then?
As an example, think about sets.. They are iterables but not sequences..
You cannot index sets, and therefore cannot slice them..

How do we do the above said unpacking then ?

Python provides the `*` exactly for this

```python

s = {1,2,3,4,5}
a, *b = s

print(a, type(a)) #1 , int
print(b, type(b)) #[2,3,4,5] , list

'''
VERY IMPORTANT to notice that b is a list, even though we unpacked a set.
Extended Unpacking always creates a **list** for the starred variable.
'''

```

## `*` operator on RHS!!

The asterisk (*) does two opposite things in Python depending on where you put it. 
When in RHS,you are unpacking a single iterable out into separate items, 
whereas in LHS (eg: a, *b = l), you are packing leftover items into a list.

```python

l1 = [1,2,3]
l2 = [4,5,6]

l = [*l1, *l2]  #[1,2,3,4,5,6]

```


```python

a, *b = [1,2,3,4,5]
a, *b = (1,2,3,4,5)
a, *b = 'XYZ'

a, b, *c = 1,2,3,4,5
a, b, *c, d = [1,2,3,4,5]

a, *b, c, *d = [1,2,3,4,5,6,7]  # SyntaxError: multiple starred expressions in assignment
```

It's pretty obvious that extended unpacking works on all iterables,
just remember that since `*` means 'everything else' , you cannot have more than
one starred variable on the LHS.. It makes no logical sense to have more than one,
and hence a syntax error will be raised.

But what about something like this?

```python

a, *b, (c, *d) = [1,2,3, 'python']

#This is perfectly valid because even though at first glance it looks like
# two * operators on LHS, it is infact a nested operation. So it makes logical sense

# a = 1
# b = [2,3]
# c, *d = 'python'
### c = 'p'
### d = ['y', 't', 'h', 'o', 'n']

```

Unpacking works the exact same way irrespective of the type of iterable (ordered vs unordered).
But by the very nature of unordered iterables, we cannot guarentee the order.
So we rarely ever use unpacking with unordered iterables.

```python

d1 = {'key1', 'key2'}
d2 = {'key3', 'key4'}

# I now want a list of all items  from above sets.. I dont care about order, How ?
# Simple, use unpacking

l = [*d1, *d2]

```


---
