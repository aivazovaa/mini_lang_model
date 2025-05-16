import re
from train import train
from generate import generate
from template_builder import apply_template


def print_help():
    print("""
===============================
 Mini Language Model — HELP
===============================

Supported Syntax:

STATEMENTS:
  FOR       e.g.  for (int i = 0; i < 5
  IF        e.g.  if (x >= 1
  ASSIGN    e.g.  x = y + 1
  PRINT     e.g.  print(i)

VARIABLES:
  x, y, i, j

VALUES:
  0, 1, 2, 5, 10

ARITHMETIC OPERATORS:
  +, -

COMPARISON OPERATORS:
  <, >, <=, >=, ==, !=

Examples:
  for (int i = 1; i < 10
    → ['FOR', 'i', '1', '10']

  if (x != 0
    → ['IF', 'x', '!=', '0']

  x = y + j
    → ['ASSIGN', 'x', 'y', '+', 'j']

  print(y)
    → ['PRINT', 'y']

Partial input is accepted, but must be syntactically valid.
Press Ctrl+C to exit.
""")


def parse(user):
    user = user.strip()


    m = re.match(r'for\s*\(\s*(?:int\s+)?([xyij])\s*=\s*(\d+)\s*;\s*\1\s*<\s*(\d+)', user)
    if m:
        return ['FOR', m.group(1), m.group(2), m.group(3)]

    m = re.match(r'for\s*\(\s*(?:int\s+)?([xyij])\s*=\s*(\d+)', user)
    if m:
        return ['FOR', m.group(1), m.group(2)]


    m = re.match(r'for\s*\(\s*(?:int\s+)?([xyij])', user)
    if m:
        return ['FOR', m.group(1)]

    m = re.match(r'if\s*\(\s*([xyij])\s*(<=|>=|==|!=|<|>)\s*([xyij0-9]+)', user)
    if m:
        return ['IF', m.group(1), m.group(2), m.group(3)]


    m = re.match(r'if\s*\(\s*([xyij])\s*(<=|>=|==|!=|<|>)', user)
    if m:
        return ['IF', m.group(1), m.group(2)]

    m = re.match(r'if\s*\(\s*([xyij])', user)
    if m:
        return ['IF', m.group(1)]


    m = re.match(r'([xyij])\s*=\s*([xyij])\s*([+-])\s*([xyij0-9]+)', user)
    if m:
        return ['ASSIGN', m.group(1), m.group(2), m.group(3), m.group(4)]

    m = re.match(r'([xyij])\s*=\s*([xyij])\s*([+-])\s*$', user)
    if m:
        return ['ASSIGN', m.group(1), m.group(2), m.group(3)]

    m = re.match(r'([xyij])\s*=\s*([xyij])$', user)
    if m:
        return ['ASSIGN', m.group(1), m.group(2)]

    m = re.match(r'([xyij])\s*=\s*$', user)
    if m:
        return ['ASSIGN', m.group(1)]

    m = re.match(r'print\s*\(\s*([xyij])\s*\)', user)
    if m:
        return ['PRINT', m.group(1)]

    return []


if __name__ == '__main__':
    print_help()
    model = train()
    print("Done training")
    while True:
        try:
            u = input(">>> ")
            t = parse(u)
            if not t:
                print("Неверный ввод.")
                continue
            c = generate(model, t)
            seq = t + c
            print("TOK:", seq)
            print(apply_template(seq))
        except KeyboardInterrupt:
            break
