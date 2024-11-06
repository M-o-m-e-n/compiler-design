import re

# Token specification
token_specification = [
    ('comment', r'//.*'),  # Single-line comments
    ('multiline_comment', r'/\*[\s\S]*?\*/'),  # Multi-line comments
    ('keyword', r'\b(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|string|class|struct|include)\b'),  # C keywords
    ('identifier', r'[A-Za-z_][A-Za-z0-9_]*'),  # Identifiers
    ('numeric_constant', r'\d+(\.\d*)?([eE][+-]?\d+)?'),  # Integer, decimal, or scientific notation
    ('operator', r'==|!=|<=|>=|\+\+|--|[+\-*/=<>]'),  # Operators including comparison
    ('special_character', r'[@#$;(){}.,\[\]&]'),  # Special characters
    ('angle_bracket', r'<|>'),  # Angle brackets for #include
    ('string', r'\"(\\.|[^"\\])*\"'),  # String literals with escaped characters
    ('newline', r'\n'),  # Line endings
    ('skip', r'[ \t]+'),  # Skip over spaces and tabs
]

# Create the regex pattern by combining the token specification
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

def lex(source_code):
    line_number = 1
    tokens = []

    # Use regex to find matches for each token in the source code
    for match in re.finditer(token_regex, source_code):
        kind = match.lastgroup
        value = match.group()
        
        # Handle line number increments
        if kind == 'newline':
            line_number += 1
        elif kind == 'skip':
            continue  # Ignore spaces and tabs
        else:
            tokens.append((kind, value, line_number))

    return tokens
    
# Accept multiline input from the user
print("Enter the C code (type 'END' on a new line to finish):")
lines = []
while True:
    line = input()
    if line.strip().upper() == 'END':
        break
    lines.append(line)

source_code = '\n'.join(lines)

# Lex the source code and print the tokens
tokens = lex(source_code)

for token in tokens:
    print(token)
    
# Wait before closing
input("Press Enter to close...")
