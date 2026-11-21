# Peephole Optimizations

Happens at Compile time
Basically python tries to optimize run time speed by
precalculating some stuff at compile time, rather that
let is get re-calculated every time the program runs..

## What gets optimized

1. Constane expressions
    - Numeric calculations (eg: 24 *60 -> python precalculates this to 1440)
    - Short sequences with length < 20 (eg: 'abc'*3 ; 'hello' + 'world' etc) 

2. Membership Tests: Mutables are replaced by Immutables
    - READ ABOUT THIS ONLINE.

`my_func.__code__.co_consts`
