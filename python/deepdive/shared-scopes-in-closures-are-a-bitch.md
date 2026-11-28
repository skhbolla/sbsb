```python

adders = []

for i in range(0,3):
    adders.append(lambda x: x + i)

adders[0](1)
adders[1](1)
adders[2](1)

```

What would the above code do ?

If you expect the answer to be 1 , 2 , 3
YOU ARE WRONG!!!


But why ?

- It is obvious that during every iteration of for loop, a closure is created (ofc, because the lambda is referencing a free variable)
- After the first iteration, the first closure's shared cell points to i  (which belongs to global scope here ... THIS IS VERY IMPORTANT to realize)
- After second iteration, the second closure's shared cell points to the same global i (which now hold value 1)
- After third iteration, the third closure's shared cell points to the same global i (which now holds value 2)

now when you run the adders , they have their own shared cells, BUT all those shared cells now point to the same global i
whose value is 2 (because iteration stopped at i = 2)

Hence the output will be 3 , 3 , 3
