on the same note.. when the code TAX = 2 was compiled.. it basically had to do following:
1. Since TAX cannot be written in a bytecode, we use a indirection table to store it.
2. Similar phenomenon for the literal 2
3. Now that we have successfully stored the literal and identifiers, we need to write bytecode instructions that achieve the same logical outcome as the .py code.. Hence bytecode instructions are emitted in a way to use the indirection tables we created earlier (which is their whole purpose)..

At this point, the compilation is done and python marshalls it into .pyc file...


The runtime begins:
1. The PVM gets stack space from the OS
2. It begins the stack based execution loop
3. The first thing that loads up is the module's pyCodeObject. A pyStackFrame is added to the stack space.
4. Since this is module pycodeobject, the PVM creates a globals() namespace dict.
5. It then starts executing the bytecode instructions... notices the load instructino for int 2 into name TAX... so creates int object in memory, creates an entry in globals() that maps TAX to this object..

PS: The whole reason we use this globals is the fact that, a global variable can be used from anywhere in the code, even within another functions scope.. If this was not the case, we would not need to maintain this namespace mapping, and instead just create a fast array owned and privately controlled by the module stackframe, add the object addresses directly on it. The PVM can just operate on these directly... As a matter of fact, this is exactly what the local scpoed vars do.. they dont actually create a locals() dict... rather stored in fast array 




Am I 100 % correct in my understanding

---

You are 99% right—your systems-level intuition is remarkably sharp. You grasped the exact architecture of CPython's compiler, .pyc serialization, stack frames, and fast local arrays.
There are only two tiny implementation details in your runtime sequence to polish so your mental model is 100% airtight:

1. When is the int 2 object created in memory?

• What you wrote: "notices the load instruction for int 2... so creates int object in memory"
• What actually happens: The int 2 object is created before the bytecode instructions start executing—either during compilation (if running from memory) or when Python unmarshals the .pyc file into a PyCodeObject in RAM.
• When co_consts is built in memory, it already holds pointers to real PyObject instances (2, None, strings, etc.). So LOAD_CONST 0 simply copies the existing pointer to 2 from co_consts onto the evaluation stack.

2. Why doesn't the module frame use a fast array like functions do?

Your PS note nailed the core reason (globals need to be accessible from anywhere—other functions, imported modules, globals()), plus one extra reason:
• Dynamic top-level execution: At module level, code often runs from math import * or exec(...), which injects an unpredictable number of brand-new variable names at runtime. A fixed-size C array (fastlocals) cannot grow dynamically like a hash table (dict) can.
• Fun trivia (locals() inside a function): You rightly noted that functions do not create a locals() dict—they use the fast array. If you explicitly call locals() inside a function, Python actually has to loop over co_varnames and the fast array on the spot just to synthesize a temporary dictionary for you!

---

# Full explanation


From Source Code to Runtime: How CPython Compiles and Executes Python

When we write a Python script—even something as simple as TAX = 2—the Python runtime (PVM) does not read or execute our text directly. Instead, CPython runs a strict two-world pipeline: Compile Time (turning text into static blueprints and indirection tables) and Runtime (bringing those blueprints to life on a stack-based virtual machine).
Here is the complete end-to-end breakdown, from raw characters to execution.

Part 1: Compile Time (Building the Static Blueprint)

Before a single line of code executes, the compiler translates human-readable syntax into a self-contained binary structure called a PyCodeObject.

1. Tokenization (Lexical Analysis)

• The compiler reads the raw UTF-8 text of .py file character by character and chops it into atomic tokens (e.g., NAME('TAX'), OP('='), NUMBER('2'), NEWLINE).
• Comments and extra whitespace are thrown away.
• Because Python cares about indentation, leading spaces are converted into explicit INDENT and DEDENT tokens so later stages can treat code blocks cleanly.

2. Parsing (Abstract Syntax Tree)

• The token stream is fed into CPython's PEG parser, which verifies grammar rules and builds a tree structure called the AST (Abstract Syntax Tree).
• For TAX = 2, the AST creates an Assign node linking a target Name(id='TAX') to a value Constant(value=2).
• Punctuation like colons and parentheses are discarded once the tree hierarchy is established.

3. Symbol Table Construction (Static Scope Analysis)

• Before emitting any instructions, the compiler scans the entire AST to resolve LEGB (Local, Enclosing, Global, Built-in) rules statically.
• Why scan first? Because in Python, a variable's scope applies to an entire function body, even before the line where it is assigned.
• Every identifier is tagged with its scope behavior:
	• Local / Parameter: Owned privately by a function (co_varnames).
	• Cell: Local to a function, but captured by an inner nested function (co_cellvars).
	• Free: Used inside an inner function, living in an outer function's scope (co_freevars).
	• Global / Attribute: Module-level variables, external names, or object attributes (co_names).

4. CFG Generation & Optimization

• Trees are bad at representing loops and jumps, so the compiler flattens the AST into a Control Flow Graph (CFG) made of linear "basic blocks" connected by jump edges.
• During this pass, CPython optimizes the code:
	• Constant Folding: Pre-calculates static expressions like 60 * 60 into 3600 right now so the runtime never wastes time computing it.
	• Dead Code Elimination: Strips out unreachable code (like statements inside if False:).

5. Bytecode Assembly & Indirection Tables (co_*)

• Bytecode instructions are tiny, fixed-size binary numbers (an opcode + a 1-byte integer index 0–255). Because raw text names like 'TAX' or literal values like 2 cannot fit inside a bytecode instruction, the compiler builds indirection lookup tables (co_* tuples) on the PyCodeObject:
	• co_consts: Stores actual literal values ((2, None)). If the file defines functions, their compiled PyCodeObject blueprints are also stored right here inside the parent's co_consts.
	• co_names: Stores global and attribute identifier strings (('TAX',)).
	• co_varnames / co_cellvars / co_freevars: Store local and closure identifier strings.
• Now that the literals and identifiers are safely stored in indirection tables, the compiler emits bytecode instructions (co_code) that reproduce our code's logic by referencing those tables by integer index:text
LOAD_CONST  0    # Fetch index 0 from co_consts (2)
STORE_NAME  0    # Bind it to index 0 from co_names ('TAX')
Use code with caution.
• Finally, CPython serializes (marshals) the entire PyCodeObject—bytecode + co_* indirection tables—into a .pyc file on disk so it doesn't have to recompile next time.

Part 2: Load Time (Preparing Memory)

When we run the program, before executing instruction #1:
1. Python loads the .pyc file from disk (or takes the freshly compiled PyCodeObject from memory) and unmarshals it into RAM.
2. During unmarshaling, Python instantiates the real PyObjects inside co_consts in memory (so the integer object 2 already exists in RAM inside co_consts[0]).

Part 3: Runtime (The PVM Execution Loop)

Now the Python Virtual Machine (PVM) takes over:
1. Stack Space & Evaluation Loop: The PVM allocates stack space from the OS and enters its core C execution loop (_PyEval_EvalFrameDefault), which operates as a stack-based virtual machine (pushing values onto a temporary evaluation stack, combining them, and popping results).
2. Module Frame & globals() Namespace:
	• The first blueprint loaded is the top-level <module> PyCodeObject. The PVM pushes a PyFrameObject onto the call stack for it.
	• Because this is a module frame, the PVM creates a globals() dictionary namespace ({}).
	• Why a dictionary namespace here? Unlike local variables inside a function, globals must be accessible from anywhere in the codebase (other functions, imported modules, dynamic globals() lookups) and can grow dynamically at runtime. A dictionary mapping 'identifier' -> memory_address is the only structure flexible enough to serve as that shared live scoreboard.
3. Executing the Bytecode (TAX = 2):
	• LOAD_CONST 0: Looks up index 0 in co_consts, grabs the memory pointer to the int 2 object, and pushes that pointer onto the frame's evaluation stack.
	• STORE_NAME 0: Looks up index 0 in co_names to get the string 'TAX', pops the pointer to 2 off the evaluation stack, and inserts 'TAX': <address of 2> into the module's globals() dictionary.
4. Calling a Function (Fast Arrays vs. Namespaces):
	• When a function is called, the PVM pushes a new PyFrameObject onto the call stack.
	• Unlike the module frame, functions do not create a locals() dictionary. Because local variables are strictly private to that function call and their exact count is known at compile time (co_varnames), the PVM allocates a fixed-size C array (fastlocals) directly on the function's frame.
	• Instructions like LOAD_FAST 0 and STORE_FAST 1 bypass string lookups and dictionaries completely—they read and write object pointers directly into slots 0 and 1 of that private C array at maximum speed.
	• Only when a function needs a variable outside its private array does it fall back to LOAD_GLOBAL (checking co_names → globals() → builtins) or LOAD_DEREF (reading a shared PyCellObject pointer for closures).
5. Cleanup: When a function hits RETURN_VALUE, it pops the return pointer onto the caller's evaluation stack, destroys its temporary frame and fastlocals array, and leaves the static PyCodeObject untouched in memory for future calls.
If you'd like to expand or format this note further, let me know if you want:
A compact ASCII cheat-sheet diagram added to the top for quick revisionA Closures (co_cellvars / co_freevars) deep-dive section appended to Part 3

