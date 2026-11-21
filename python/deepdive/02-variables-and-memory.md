# Variables are Memory References

'Python Memory Manager' takes care of operations on the Heap.

Variables in python are ALWAYS references to memory addresses.
We can use `id()` function to get the memory address referenced by a variable.

---

# Reference Counting

Python Memory Manager keeps track of how many variables are referencing a object
in memory.

`sys.getrefcount(my_var)`

> Note that by passing my_var to getrefcount() creates an extra reference
> thereby increasing the ref count by 1.
> This is because all variables are passed by refernce in python.


`ctypes.c_long.from_address(address).value`

> Above solves the issue by passing the actual address rather than a variable.

# Garbage Collection

Garbage collector's primary purpose is catching and cleaning up circular references.

CPython relies on reference counting as its main mechanism to reclaim memory immediately, 
and uses the cyclic garbage collector as a secondary safety net for objects 
that reference each other in a loop.

```python

import gc

gc.get_objects() #This returns all objects being tracked by gc

gc.disable() #Disabled garbage collection

gc.collect() #Triggers garbage collection

```

> Note that garbage collectors only track container types, 
> because simple types like int, float can never hold references to other objects,
> they can never form cycles. Therefore garbage collector only tracks container types.

---

# Dynamic vs Static Typing

In statically typed languages, variables are bound to a specific type.
In dynamically typed langs, variables are purely references to memory, and have no type attached to them.

when we do `type(my_var)` , python looks up the object in memory referenced by my_var,
and infers its type. REMEBER, my_var itself has no associated type. It is purely a reference to something.


---

# Variable Re-assignment

`=` operator simply binds a variable name to whatever object the expression on the right-hand side evaluates to.

Whether id(my_var) changes after my_var = ... depends entirely on what the 
right-hand side produces, not on the `=` operator itself.

Take below code as example:

```python
l = [1, 2]
print(id(l))  # e.g., 1402348923412

# Case A: Right side creates a brand-new list object
l = l + [3]
print(id(l))  # New id (brand-new list)

# Case B: Right side returns the existing singleton 'None' object. (in-place operations return None on success)
l = l.append(3)
print(id(l))  # Different id (id of None)

```

One thing you might notice is that, this logic is pretty straight foward for immutable objects..
If I try `x = x+5` where is an int, it is pretty clear that a new int object must be created because ints are immutable in python.
Hence the id(x) will change after running this.

But for mutable objects, it might seem like `l = l.append(3)` should retain the same id.
But it is not the case... l.append(3) does in fact do an in-place update without creating any new objects,
but it returns a 'None' on success. None is a singleton object with it's own memory location.
Hence, id(l) changes... 

For `l = l + [3]` , it is very different from append because 
concatination is not a in-place operation.. It creates a new object (even though a list is mutable)
Hence, id(l) changes here too..


The BOTTOM LINE to take away is that, the `=` operator simply evaulates
the RHS first and assigns it to the variable on LHS.
Whether id changes or not fully depends on what the RHS evaulates to.

> The main trap here is the assumption that in-place operations like append
> will not modify the id upon assignment. This is wrong because even though
> append is an inplace operation that DOES NOT create a new object, it returns
> a NONE object ... This is what causes the change in id.

---

# Variable Equality

Two different meanings to equality:

1. Same memory address ? i.e same object ?  - Do this using `is`
2. Same object state (data) - Do this using `==` operator

The negation of above will be `is not` and `!=` respectively.

---



