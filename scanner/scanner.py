import re

# Token specification
token_specification = [
    ('comment', r'//.*'),  # Single-line comments
    ('multiline_comment', r'/\*[\s\S]*?\*/'),  # Multi-line comments
    ('keyword',
     r'\b(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|string|class|struc|include)\b'),
    ('identifier', r'[A-Za-z_][A-Za-z0-9_]*'),  # Identifiers
    ('numeric_constant', r'\d+(\.\d*)?([eE][+-]?\d+)?'),  # Integer, decimal, or scientific notation
    ('operator', r'==|!=|<=|>=|\+\+|--|[+\-*/=]'),  # All operators
    ('special_character', r'[@#$;(){}.]'),  # Special characters
    ('newline', r'\n'),  # Line endings
    ('skip', r'[ \t]+'),  # Skip over spaces and tabs
]

# Create the regex pattern by combining the token specification
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)


source_code =input("Enter the source code: ")

def lex(source_code):
    line_number = 1
    tokens = []

    # Create a scanner object
    for match in re.finditer(token_regex, source_code):
        kind = match.lastgroup
        value = match.group()
        if kind == 'NEWLINE':
            line_number += 1
        elif kind == 'skip' :
            continue  # Ignore  tabs
        else:
            tokens.append((kind, value, line_number))

    return tokens


# Run the lexical analyzer on the source code
tokens = lex(source_code)

for token in tokens:
    print(token)
