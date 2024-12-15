# the missing parts :
# 1\ the stack after checking when the string rejected
# 2\ parse tree

class Grammar:
    def __init__(self):
        self.rules = {}
        self.simple = False

    def add_rule(self, non_terminal, rule):
        if non_terminal not in self.rules:
            self.rules[non_terminal] = []
        self.rules[non_terminal].append(rule)

    def is_simple(self):
        # Check if the grammar is simple (no left recursion, no ambiguity)
        for non_terminal, rules in self.rules.items():
            for rule in rules:
                if rule[0] == non_terminal:
                    self.simple = False  # Left recursion detected
                    return False
        self.simple = True
        return True


class TopDownParser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.input_string = []
        self.index = 0
        self.stack_after_checking = []

    def parse(self, non_terminal):
        if self.index >= len(self.input_string):
            return False

        for rule in self.grammar.rules.get(non_terminal, []):
            saved_index = self.index
            if self.match_rule(rule):
                return True
            self.index = saved_index

        return False

    def match_rule(self, rule):
        for symbol in rule:
            if symbol.isupper():  # Non-terminal
                if not self.parse(symbol):
                    return False
            else:  # Terminal
                if self.index < len(self.input_string) and self.input_string[self.index] == symbol:
                    self.index += 1
                else:
                    return False
        return True

    def check_string(self, input_string):
        self.input_string = list(input_string)
        self.index = 0
        is_accepted = self.parse(next(iter(self.grammar.rules))) and self.index == len(self.input_string)

        # Update stack after checking
        if is_accepted:
            self.stack_after_checking = []  # Accepted: stack is empty
        else:
            self.stack_after_checking = self.input_string[self.index:]  # Rejected: remaining part in stack

        # Display results
        print(f"The input string: {self.input_string}")
        print(f"The stack after checking: {self.stack_after_checking}")
        print(f"The rest of unchecked string: {self.stack_after_checking}")

        return is_accepted


if __name__ == "__main__":
    while True:
        print("\n1. Enter Grammar\n2. Check String\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            grammar = Grammar()
            print("The grammar must have exactly 2 non-terminals, each with exactly 2 rules.")

            for _ in range(2):  # Limit to exactly 2 non-terminals
                non_terminal = input("Enter non-terminal: ")
                grammar.rules[non_terminal] = []  # Ensure no extra rules are added

                print(f"Enter 2 rules for the non-terminal '{non_terminal}':")
                for i in range(2):  # Limit to exactly 2 rules per non-terminal
                    rule = input(f"Rule {i + 1}: ").strip()
                    grammar.add_rule(non_terminal, rule)

            if grammar.is_simple():
                print("The Grammar is simple.")
            else:
                print("The Grammar isn't simple. Please re-enter the grammar.")

        elif choice == "2":
            if 'grammar' not in locals():
                print("Please define a grammar first.")
                continue

            if not grammar.simple:
                print("The grammar isn't simple. Please enter a valid grammar first.")
                continue

            input_string = input("Enter the string to be checked: ")
            parser = TopDownParser(grammar)

            if parser.check_string(input_string):
                print("Your input string is Accepted.")
            else:
                print("Your input string is Rejected.")

        elif choice == "3":
            break

        else:
            print("Invalid choice. Please try again.")
