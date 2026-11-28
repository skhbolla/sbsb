#!/usr/bin/env python3
import dis
import marshal
from pathlib import Path
import py_compile
import sys

def format_value(val):
  """Pretty-format a value with its exact runtime type."""
  t_name = type(val).__name__
  if hasattr(val, "co_code"):
    return f"<code object {val.co_name}>"
  return f"({t_name}) {repr(val)}"

def dump_code_object(co, depth=0):
  indent = "  " * depth
  prefix = f"{indent}├── "
  sub_indent = f"{indent}│   "

  print(f"\n{indent}{'='*60}")
  print(
      f"{indent}PyCodeObject: <{co.co_name}>  [Line {co.co_firstlineno} in"
      f" {co.co_filename}]"
  )
  print(f"{indent}{'='*60}")

  # 1. Structural Sizing & Layout Metadata
  print(f"{prefix}co_argcount:        {co.co_argcount} (Positional params)")
  print(
      f"{prefix}co_posonlyargcount: {co.co_posonlyargcount} (Positional-only"
      " params)"
  )
  print(
      f"{prefix}co_kwonlyargcount:  {co.co_kwonlyargcount} (Keyword-only"
      " params)"
  )
  print(
      f"{prefix}co_nlocals:         {co.co_nlocals} (Total local variable"
      " slots)"
  )
  print(
      f"{prefix}co_stacksize:       {co.co_stacksize} (Max evaluation stack"
      " depth)"
  )
  print(
      f"{prefix}co_flags:           {bin(co.co_flags)} ->"
      f" {dis.pretty_flags(co.co_flags)}"
  )

  # 2. Local Variable Slots (Fast C Array in Frames)
  print(f"{prefix}co_varnames:        {co.co_varnames}")
  for idx, name in enumerate(co.co_varnames):
    print(f"{sub_indent}  slot [{idx}] -> '{name}'")

  # 3. Global / Built-in / Attribute Names Table
  print(f"{prefix}co_names:           {co.co_names}")
  for idx, name in enumerate(co.co_names):
    print(f"{sub_indent}  name [{idx}] -> '{name}'")

  # 4. Closures & Scopes (Free and Cell variables)
  print(
      f"{prefix}co_cellvars:        {co.co_cellvars} (Captured by inner"
      " functions)"
  )
  print(
      f"{prefix}co_freevars:        {co.freevars if hasattr(co, 'freevars') else co.co_freevars} (Borrowed from outer functions)"
  )

  # 5. Literal Constants Pool
  print(f"{prefix}co_consts:          (length: {len(co.co_consts)})")
  nested_code_objects = []
  for idx, const in enumerate(co.co_consts):
    print(f"{sub_indent}  const [{idx}] = {format_value(const)}")
    if hasattr(const, "co_code"):
      nested_code_objects.append(const)

  # 6. Raw Bytecode Instructions & Opcodes
  print(f"{prefix}co_code (raw byte integers):")
  print(f"{sub_indent}  {list(co.co_code)}")

  print(f"{prefix}co_code (decoded 2-byte word stream):")
  code_bytes = co.co_code
  for offset in range(0, len(code_bytes), 2):
    opcode = code_bytes[offset]
    oparg = code_bytes[offset + 1]
    opname = dis.opname.get(opcode, f"UNKNOWN_{opcode}")

    # Resolve human-readable target
    arg_repr = ""
    if opcode in dis.hasconst and oparg < len(co.co_consts):
      arg_repr = f"-> {format_value(co.co_consts[oparg])}"
    elif opcode in dis.hasname and oparg < len(co.co_names):
      arg_repr = f"-> '{co.co_names[oparg]}'"
    elif opcode in dis.haslocal and oparg < len(co.co_varnames):
      arg_repr = f"-> fastlocals[{oparg}] ('{co.co_varnames[oparg]}')"

    print(f"{sub_indent}  {offset:04d}: {opname:<20} {oparg:<5} {arg_repr}")

  # Recursively dump nested functions, lambdas, and classes found in co_consts
  for nested_co in nested_code_objects:
    dump_code_object(nested_co, depth + 1)

def inspect_py_file(filepath):
  target = Path(filepath)
  if not target.exists():
    print(f"Error: File '{target}' does not exist.", file=sys.stderr)
    sys.exit(1)

  print(f"\n[*] Reading and compiling '{target}'...")
  source_code = target.read_text(encoding="utf-8")

  # Compile text into the root <module> PyCodeObject
  root_code = compile(source_code, str(target), "exec")

  # Alternatively, compile to disk and unmarshal from the .pyc:
  # pyc_path = py_compile.compile(str(target))
  # with open(pyc_path, "rb") as f:
  #     f.read(16)  # Skip 16-byte header
  #     root_code = marshal.load(f)

  dump_code_object(root_code)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print(f"Usage: python3 {Path(__file__).name} <target_file.py>")
    sys.exit(1)

  inspect_py_file(sys.argv)
