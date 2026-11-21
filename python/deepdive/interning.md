# Integer Interning
When a python program first launches, integers in the range
of [-5 to 256] are created as objects in memory before even
a single instruction from our code is executed.

Python calls this the global pool cache. When we create a integer
within in range later in the code, python will simply reuse
the object from global pool. 

This creates the unintended side effect demonstrated nicely below

```python

a = 4068
b = 4068

print(id(a), id(b)) 
# As expected the memory addresses will be different
# because new objects are created during each assignment


c = 123
d = 123
print(id(c), id(d))
#This will produce the same memory address for both c and d
#This happens because python cached prebuilt objects for
#integers ranging between -5 and 256, and reused them for c and d


```

Why does python do this ? Simple, speed...
Python assumes that numbers between -5 and 256 are used often enough,
that it justifies having a optimization like this.

Important thing to note here:
In above example now c and d point to same mem address ie a shared reference.
Think about what happens if I now try to do `c = c+1`
Does d get effected ? 
NO!! Remember int are immutable, so the act of trying to modify the object pointed
to by c, will create a new object instead. Hence d remains uneffected.

This shared reference is acceptable here purely because int are immutable,
and we will run into unintended side effects..

---

# String Interning

Python also interns strings... WTF!! Are there strings that are so commonly
used that they justify being interned during program launch??

NO !! String interning is NOT done during launch... It does not even make sense
to intern them at launch because there are no "commonly used" strings to create and keep in cache.


Rather, string interning is done during compilation. Take below example

```python

a = 2244
b = 2244

print(a == b)

```
Think about what python does here... It checks the int object referenced by a,
then checks the int object referenced by b,
and compares the internal state of both objects using a simple number comparison..
Easy enough to do.

But consider the string equivalent of the same logic

```python

a = 'hello_world'
b = 'hello_world'

print(a == b)

```
What does python do now? 
Well it checks the string object referenced by a,
then checks the string object referenced by b,
and compares **CHARACTER-BY-CHARACTER** whether both strings are same or not..

This char by char check is pretty costly... What would you do to optimize this?

Well, when python first sees the 'hello_world' string literal during a's object creation,
it interns it. Then when it sees that b is also using the same literal,
it smartly figures out that it can reuse the same underlying object...
Hence b is also smartly pointed to same object.

A VERY IMPORTANT NOTE:
DO NOT DEPEND ON STRING INTERNING... It will not work on all strings.
Python has a lot of intricacies on what strings are interned,
so it is good to know this concept, but never really depend on string interning at all..

BUT if you do decide that you need this interning, you can explicitly force it by using
`sys.intern()` method ...


NOTE: Again, string interning creates shared references, but is still safe because
strings in python are immutable, so if one reference tries to modify it, a new object
is created rather than in-place. So all other references are safe.

---

String interning is a memory optimization technique in Python (specifically CPython) where only one copy of each distinct, immutable string is stored in a shared pool. Instead of creating duplicate string objects in memory every time the same text appears, multiple variables simply point to the exact same memory address.

Why String Interning Is Done

• Saves memory. Programs often repeat the same variable names, dictionary keys, and keywords thousands of times. Storing one shared copy instead of thousands of identical objects prevents unnecessary memory bloat.
• Speeds up dictionary lookups. Python relies heavily on dictionaries for namespaces, classes, and modules. Because interned strings are guaranteed to have unique memory addresses, Python can compare them by checking their memory pointers (is) rather than comparing them character by character (==).

When String Interning Is Done

• At compile time. Python automatically interns strings that look like valid identifiers (containing only ASCII letters, digits, and underscores) when compiling code into bytecode. Variable names, function names, and attribute names are always interned.
• For small or special strings. Empty strings ("") and single-character ASCII/Latin-1 strings (like "a" or "!") are pre-allocated and cached globally when the interpreter starts.
• Manually at runtime. You can force Python to intern any string at runtime by passing it to sys.intern().

How String Interning Is Done

• The global interned dictionary. Under the hood, CPython maintains an internal hash table (a C-level dictionary) called interned.
• Lookup before allocation. When Python decides to intern a string, it calculates its hash and checks the interned dictionary.
• Pointer reuse. If the string already exists in the dictionary, Python discards the new string and returns a pointer to the existing object. If it is not found, Python adds the new string to the dictionary and returns its pointer.
• Garbage collection. Since Python 3, interned strings are stored using weak or mortal references inside the internal dictionary. If all variables referencing an interned string are deleted, the string can still be garbage-collected to prevent memory leaks.

---

Important Caveats

• Code block (AST) constant folding. If you define two identical non-interned strings (like a = "hello world" and b = "hello world") within the same function or code block, a is b may still evaluate to True. This is not string interning; it is Python's compiler reusing constants within the same code object. Across separate functions or modules, a is b will be False.
