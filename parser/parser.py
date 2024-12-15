class Grammar:
    def __init__(self):
        self.rules = {}
        self.simple = False

    def add_rule(self, non_terminal, rule):
        if non_terminal not in self.rules:
            self.rules[non_terminal] = []
        self.rules[non_terminal].append(rule)

    def is_simple(self):
        # Check if the grammar is simple (no left recursion, no ambiguity, no empty rules)
        for non_terminal, rules in self.rules.items():
            rule_starts = []  # Store the starting symbols of the rules for duplicate terminal check
            for rule in rules:
                if rule == "":  # Check for empty rules
                    self.simple = False
                    return False
                if rule[0] == non_terminal:  # Check for left recursion
                    self.simple = False
                    return False
                if rule[0].isupper():  # Check if the rule starts with a non-terminal (left recursion check)
                    self.simple = False
                    return False

                # Check for duplicate terminals in different rules of the same non-terminal
                if rule[0] in rule_starts:
                    self.simple = False
                    return False
                rule_starts.append(rule[0])

        self.simple = True
        return True


class TopDownParser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.input_string = []
        self.index = 0  # a pointer to the current index in the input string during parsing
        self.parse_tree = None  # Root of the parse tree (Holds the structure of the parse tree)

    def parse(self, non_terminal):
        """ Attempt to parse the input starting from a non-terminal. """
        if self.index >= len(self.input_string):  # this means the entire string has been consumed
            # Return a node showing the partial progress
            return {"name": non_terminal, "children": []}

        last_valid_node = {"name": non_terminal, "children": []}  # Store the partial progress

        for rule in self.grammar.rules.get(non_terminal, []):
            saved_index = self.index
            node = {"name": non_terminal, "children": []}  # Node for the current rule

            if self.match_rule(rule, node["children"]):
                return node  # Parsing succeeded with this rule

            # Backtrack and keep the most recent failed state
            self.index = saved_index
            last_valid_node = node

        # Return the partial state of the parse tree on failure
        return last_valid_node

    def match_rule(self, rule, children):
        """ Match a rule and build the tree recursively. """
        for symbol in rule:
            if symbol.isupper():  # Non-terminal
                child_node = self.parse(symbol)  # Recursively parse the non-terminal
                if child_node:
                    children.append(child_node)  # Add the child node to the parent
                else:
                    return False  # Parsing failed
            else:  # Terminal
                if self.index < len(self.input_string) and self.input_string[self.index] == symbol:
                    children.append({"name": symbol, "children": []})  # Add the terminal to the tree
                    self.index += 1
                else:
                    return False  # Terminal mismatch
        return True

    def check_string(self, input_string):
        self.input_string = list(input_string)
        self.index = 0
        self.parse_tree = []  # Reset parse tree

        root_non_terminal = next(iter(self.grammar.rules))  # Start parsing from the first non-terminal in the grammar
        parse_result = self.parse(root_non_terminal)

        is_accepted = parse_result and self.index == len(self.input_string)

        # Display results
        print(f"\nThe input string: {self.input_string}")  # Display input as a list of characters

        if is_accepted:
            print("\nParse Tree:")
            self.display_tree([parse_result])  # Display the parse tree (only if accepted)
            print("\nYour input string is Accepted.")
        else:
            print("\nYour input string is Rejected.")

        # Update stack after checking
        self.stack_after_checking = self.input_string[self.index:]
        print(f"\nThe stack after checking: {self.stack_after_checking}")

    def display_tree(self, nodes, prefix="", is_last=True):
        """ Recursively print the parse tree using lines and branches. """
        for i, node in enumerate(nodes):
            connector = "└── " if is_last and i == len(nodes) - 1 else "├── "
            print(f"{prefix}{connector}{node['name']}")
            if "children" in node and node["children"]:
                extension = "    " if is_last else "│   "
                self.display_tree(node["children"], prefix + extension, i == len(nodes) - 1)


if __name__ == "__main__":
    while True:
        print("\n1. Enter Grammar\n2. Check String\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            grammar = Grammar()

            # Always ask for 'S' and 'B' non-terminals
            print("Enter rules for non-terminal 'S':")
            for i in range(2):  # Always exactly 2 rules for 'S'
                rule = input(f"Enter rule number {i + 1} for non-terminal 'S': ").strip()
                grammar.add_rule("S", rule)

            print("Enter rules for non-terminal 'B':")
            for i in range(2):  # Always exactly 2 rules for 'B'
                rule = input(f"Enter rule number {i + 1} for non-terminal 'B': ").strip()
                grammar.add_rule("B", rule)

            if grammar.is_simple():
                print("The Grammar is simple.")
            else:
                print("The Grammar isn't simple.")

        elif choice == "2":
            if 'grammar' not in locals():
                print("Please define a grammar first.")
                continue

            if not grammar.simple:
                print("The grammar isn't simple.")
                continue

            input_string = input("Enter the string to be checked: ")
            parser = TopDownParser(grammar)

            parser.check_string(input_string)

        elif choice == "3":
            break

        else:
            print("Invalid choice. Please try again.")
