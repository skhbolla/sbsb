# Arguments vs Parameters

We define what parameters are needed when defining a function.
We pass (by reference ofc) arguments to functions when invoking them.

```python

def func(a,b): #Here a and b are called the parameters
    print(f"a = {a} , b = {b}")

func(1,2)  #Here 1 and 2 are the arguments.

x = 3
y = 4
func(x, y) #x and y are the arguments


#Note that python ALWAYS does pass by reference i.e args are
#always passed as memory addresses to the actual object
# This even applies when passing 1,2 because they are integer objects rather than primitive values.
```

---

# Positions vs Keyword arguments

## Positional Arguments

```python
def func(a,b):
    print(f"a = {a}, b = {b}")

func(10,20)
func(20,10) 

#Above, the order of arguments matters because python assigns the arguments
#to the function parameters based on the order.
```

Python also provides the option to set default values to parameters.

```python
def func(a, b= 10)
    print(a,b)

func(1) #Prints 1,10
func(1,2) #Print 1,2

```

Consider the below scenario then:

```python

# Below code will result in error
# SyntaxError: parameter without a default follows parameter with default

def func(a, b=2, c):
    print(a, b, c)

```

Think about how you would call this function 
without passing a value to b (i.e use the default value of b)?

`func(1,3)` -> If you do this, how would python know if 3 was the argument for b or c ?

This is exactly why python never allows params without default values to 
follow after a param with default value..

In other words, all your default value parameters must be at the end of function signature.

KEYWORD ARGUMENTS (also called NAMED ARGUMENTS) can help with above problem...

## Keyword arguments

```python

def func(a, b=2, c):
    print(a,b,c)

func(1,2,3) #Positional arguments
func(a=1, b=2, c=3) #Keyword arguments
func(c=3, a=1, b=2) #Keyword arguments, so order does NOT matter.
func(a=1, c=3) #Keyword arguments with default value
func(1, c=3) #Still valid, a will be 1, b is default, c will be 2


func(c=1, 2, 3) #INVALID, will raise error
func(1, b=2, 3) #INVALID, will raise error
# Once a named argument is used, all arguments thereafter must be named too..

```

---
