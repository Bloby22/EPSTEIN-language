# EPSTEIN Language (Python)

**EPSTEIN** is a custom programming language with Python-like indentation syntax.  
It is executed via a Python interpreter, allowing `.epc` files to be run directly.

---

## 1️⃣ Features

- Indentation-based syntax similar to Python
- Custom keywords mapped to runtime values
- Built-in functions like `files`, `risk`, `theory`, `money`
- Supports loops, conditionals, and function blocks
- Extendable runtime with custom Python functions

---

## 2️⃣ Variable & Token Mapping

| EPSTEIN    | Python mapping / runtime          |
|------------|---------------------------------- |
| truth      | True                              |
| lie        | False                             |
| deal       | str                               |
| alibi      | None                              |
| files      | print()                           |
| theory     | float() / int()                   |
| suicide    | return / sys.exit()               |
| money      | bool()                            |
| famous     | function                          |
| girl       | dict                              |
| island     | list                              |
| plot       | def / block                       |
| shadow     | lambda                            |
| risk       | float()                           |
| secret     | set()                             |
| enemy      | dict                              |
| weapon     | list                              |
| mission    | tuple                             |
| power      | int                               |
| ghost      | str                               |
| time       | int                               |
| light      | bool                              |
| government | dict                              |
| universe   | None                              |
| circle     | lambda                            |
| escape     | break / sys.exit()                |
| crew       | list                              |
| plan       | def / block                       |
| agenda     | dict                              |
---

## 3️⃣ Syntax Examples

### Variable assignment
```epstein
deal = "Classified"
power = 9000
truth = truth
````

### Print / Output

```epstein
files "Hello world"
files deal
```

### Conditionals

```epstein
if truth:
    files "Approved"
else:
    files "Denied"
```

### Loops

```epstein
crew = ["Alice", "Bob"]

loop crew:
    files item
```

Equivalent Python:

```python
for item in crew:
    print(item)
```

### Function Blocks

```epstein
plot infiltration:
    files "Inside base"

plan escape:
    files "Escape started"
```

---

## 4️⃣ Installation

Install via pip (once published):

```bash
pip install epstein
```

Or run locally:

```bash
git clone https://github.com/bloby22/EPSTEIN-language
cd epstein
python -m pip install .
```

---

## 5️⃣ Usage

```python
from epstein import Interpreter, parse_file

program = parse_file("script.eps")
interpreter = Interpreter()
interpreter.execute(program)
```

---

## 6️⃣ Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 7️⃣ License

MIT License
