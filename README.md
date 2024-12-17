# Scanner - The First Phase of Compiler Design

## Project Overview
This project implements the **Scanner** (or **Lexical Analyzer**) phase of a compiler, responsible for reading source code and breaking it down into meaningful tokens.
The Scanner identifies keywords, identifiers, operators, literals, and other language constructs, setting up the groundwork for further stages in the compilation process.

## Features
- **Tokenization**: Recognizes and extracts tokens such as keywords, identifiers, operators, numbers, and special symbols.

## How It Works
1. **Input**: The Scanner reads a source code file (e.g., `.c++`,`.c`).
2. **Tokenization**:
   - Utilizes regular expressions or pattern matching to scan and identify tokens.
   - Each token is categorized according to type, like `Keyword`, `Identifier`, `Operator`, etc.
3. **Output**: Generates a list of tokens with associated types for syntax analysis.

# Parser - Top-Down Parser for Context-Free Grammar

This document describes the functionality and usage of the `Grammar` and `TopDownParser` classes implemented in the provided code. These classes enable the creation of a context-free grammar and the implementation of a top-down parser for checking and parsing input strings based on the grammar.

---

## **1. Grammar Class**

The `Grammar` class is responsible for defining and validating a set of production rules for a context-free grammar.

### **Attributes**

- `rules`: A dictionary where the keys are non-terminals and the values are lists of production rules.
- `simple`: A boolean indicating whether the grammar is simple.

### **Methods**

#### `__init__(self)`

Initializes the `Grammar` object with empty rules and sets `simple` to `False`.

#### `add_rule(self, non_terminal, rule)`

Adds a production rule for a given non-terminal.

- **Parameters:**
  - `non_terminal` (str): A non-terminal symbol.
  - `rule` (str): A production rule.

#### `is_simple(self)`

Checks whether the grammar is simple. A grammar is simple if it satisfies the following conditions:

- No left recursion.
- No ambiguity in rules (no duplicate terminals starting different rules for the same non-terminal).
- No empty rules ("") present.

**Returns:**

- `True` if the grammar is simple, otherwise `False`.

---

## **2. TopDownParser Class**

The `TopDownParser` class performs top-down parsing based on a given grammar and checks whether an input string can be derived from the grammar.

### **Attributes**

- `grammar`: A `Grammar` object representing the grammar to parse against.
- `input_string`: A list of characters representing the string to be parsed.
- `index`: An integer pointer to the current position in `input_string` during parsing.
- `parse_tree`: A nested structure representing the parse tree.

### **Methods**

#### `__init__(self, grammar)`

Initializes the parser with the given grammar.

- **Parameters:**
  - `grammar` (Grammar): The grammar to use for parsing.

#### `parse(self, non_terminal)`

Attempts to parse the input string starting from a given non-terminal.

- **Parameters:**
  - `non_terminal` (str): The starting non-terminal.
- **Returns:**
  - A parse tree node if successful, or the last valid parse tree state on failure.

#### `match_rule(self, rule, children)`

Matches a rule against the current position in the input string and builds the parse tree.

- **Parameters:**
  - `rule` (str): The production rule to match.
  - `children` (list): A list to store child nodes of the parse tree.
- **Returns:**
  - `True` if the rule matches, otherwise `False`.

#### `check_string(self, input_string)`

Checks if the given string can be derived from the grammar and displays the parse tree.

- **Parameters:**
  - `input_string` (str): The string to be parsed.
- **Outputs:**
- Prints the parse tree and whether the string is accepted or rejected.

#### `display_tree(self, nodes, prefix="", is_last=True)`

Recursively prints the parse tree in a human-readable format.

- **Parameters:**
  - `nodes` (list): List of nodes representing the parse tree.
  - `prefix` (str): Prefix for the tree branches.
  - `is_last` (bool): Indicates if the current node is the last child.

---

## **3. Main Program Workflow**

The main program provides a user interface for interacting with the grammar and parser.

### **Options**

1. **Enter Grammar:**

   - Prompts the user to define production rules for non-terminals `S` and `B`.
   - Validates if the grammar is simple using `is_simple()`.

2. **Check String:**

   - Prompts the user for an input string.
   - Uses the `TopDownParser` to parse the string and display the results.
   - Prints the parse tree if the string is accepted.

3. **Exit:**

   - Terminates the program.

### **Key Details**

- The program requires exactly 2 rules each for `S` and `B` during grammar definition.
- Strings can only be checked if the grammar is simple.
- Provides feedback on acceptance or rejection of the input string along with a parse tree visualization.

---

## **Example Usage**

### **Defining a Grammar**

```
Enter rules for non-terminal 'S':
Enter rule number 1 for non-terminal 'S': aSB
Enter rule number 2 for non-terminal 'S': b

Enter rules for non-terminal 'B':
Enter rule number 1 for non-terminal 'B': a
Enter rule number 2 for non-terminal 'B': bBa
```

### **Checking a String**

Input: `abbaa`

```
The input string: ['a', 'b', 'b', 'a', 'a']

Parse Tree:
└── S
    ├── a
    └── S
        ├── b
        └── B
            ├── b
            └── B
                ├── a
                └── a

Your input string is Accepted.
```

Input: `abb`

```
The input string: ['a', 'b', 'b']

Your input string is Rejected.
```

---

## **Conclusion**

This implementation allows users to define a simple grammar, validate its simplicity, and parse input strings using a top-down parsing approach. The parse tree visualization provides insights into the structure of the derivation process.
