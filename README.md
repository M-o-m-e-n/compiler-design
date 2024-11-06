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
