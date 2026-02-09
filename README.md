# EPSTEIN
EPSTEIN is an experimental programming language with a mysterious, conspiracy-inspired vibe. Write `.epstein` files and run them directly using the provided TypeScript interpreter.

## Features
- Custom syntax: `.epstein` files with simple, indented blocks and unique keywords (`truth`, `lie`, `files`, `plot`, `plan`, `suicide`, `escape`, `loop`, ...).  
- TypeScript interpreter: A small interpreter (parser + runtime) written in TypeScript to load and run `.eps` scripts.  
- Readable & playful: One-word variables, clear blocks, and an intentionally odd theme for creative experiments.  
- Extensible: Add new runtime functions or tokens easily.

## Getting Started
1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/EPSTEIN-language.git
cd EPSTEIN-language
````

2. Install dependencies:

```bash
npm install
```

3. Run an `.eps` file (example):

```bash
npx ts-node src/index.ts eps/main.epstein
```

## EPSTEIN Syntax & Variables

Use one-word variable names and simple, indented blocks. Below is a quick reference of common tokens and what they map to in the runtime/TypeScript interpreter.

| EPSTEIN    | Runtime / TS mapping            | Notes                    |
| ---------- | ------------------------------- | ------------------------ |
| truth      | true                            | boolean true             |
| lie        | false                           | boolean false            |
| deal       | string                          | text / message           |
| alibi      | null                            | placeholder / none       |
| files      | Runtime.files() → console.log() | print/output             |
| theory     | Runtime.theory() → Number()     | numeric conversion       |
| suicide    | return / process.exit()         | terminate program        |
| money      | Runtime.money() → Boolean()     | boolean conversion       |
| famous     | function                        | runtime function slot    |
| girl       | object                          | generic object           |
| island     | Runtime.island() → Array        | array constructor        |
| plot       | function / block                | function block (plot:)   |
| shadow     | lambda / anonymous function     | inline small function    |
| risk       | Runtime.risk() → Number         | float/parseFloat         |
| secret     | Runtime.secret() → Set          | set constructor          |
| enemy      | object                          | generic object           |
| weapon     | Runtime.weapon() → Array        | array constructor        |
| mission    | Runtime.mission() → tuple/array | fixed list / tuple style |
| power      | number                          | numeric                  |
| ghost      | string                          | text                     |
| time       | number                          | numeric / counter        |
| light      | boolean                         | boolean                  |
| government | object                          | object/dict              |
| universe   | null                            | placeholder              |
| circle     | lambda                          | math helper              |
| escape     | break / process.exit()          | break / exit             |
| crew       | array                           | list of members          |
| plan       | function / block                | function block (plan:)   |
| agenda     | object / dict                   | mapping of steps         |

## Commands / Statements

* files "message" → print text or a variable value (calls Runtime.files() / console.log).
* plot: / plan: → define a block / function. Indent the block body.
* if <expr>: / else: → conditional blocks. Use EPSTEIN tokens in expressions.
* loop <array>: → iterate over an array; inside loop use item to refer to the current element.
* suicide → immediate program termination (maps to process.exit() in runtime).
* escape → break / exit context (maps to break or process.exit()).

## Example eps/main.eps

```
files "Mission started"
truth = true
deal = "hidden deal"

plot:
    files "Plot routine running"
    theory = 9000

if truth:
    files "The truth is revealed"
else:
    files "This is a lie"

crew = ["Alice", "Bob", "Charlie"]
loop crew:
    files item

plan:
    files deal

escape
```

## Development & Tests

Project structure:

```
epstein_project/
├─ eps/              # .epstein scripts (main.eps, missions, tests)
├─ src/              # TS interpreter, parser, runtime
│  ├─ index.ts       # entry point (run a .eps file)
│  ├─ parser.ts
│  ├─ interpreter.ts
│  └─ runtime.ts
├─ tests/            # simple tests that run .eps files
├─ package.json
├─ tsconfig.json
└─ README.md
```



Chceš, abych rovnou připravil i **verzi s emoji a tajemným konspiračním stylem**, aby vypadal víc EPSTEIN?
```
