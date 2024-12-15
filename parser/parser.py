import tkinter as tk
from tkinter import ttk, messagebox


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
        stack_after_checking = self.input_string[self.index:] if not is_accepted else []

        return is_accepted, parse_result, stack_after_checking


class GrammarParserGUI:
    def __init__(self, master):
        self.master = master
        master.title("Top-Down Parser GUI")
        master.geometry("800x600")

        self.grammar = Grammar()
        self.setup_ui()

    def setup_ui(self):
        # Grammar Rules Frame
        rules_frame = ttk.LabelFrame(self.master, text="Grammar Rules")
        rules_frame.pack(padx=10, pady=10, fill=tk.X)

        # S Non-Terminal Rules
        s_frame = ttk.Frame(rules_frame)
        s_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(s_frame, text="Rules for 'S':").pack(side=tk.LEFT)

        self.s_rules_entries = []
        for i in range(2):
            entry = ttk.Entry(s_frame, width=30)
            entry.pack(side=tk.LEFT, padx=5)
            self.s_rules_entries.append(entry)

        # B Non-Terminal Rules
        b_frame = ttk.Frame(rules_frame)
        b_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(b_frame, text="Rules for 'B':").pack(side=tk.LEFT)

        self.b_rules_entries = []
        for i in range(2):
            entry = ttk.Entry(b_frame, width=30)
            entry.pack(side=tk.LEFT, padx=5)
            self.b_rules_entries.append(entry)

        # Add Grammar Button
        add_grammar_btn = ttk.Button(rules_frame, text="Define Grammar", command=self.define_grammar)
        add_grammar_btn.pack(padx=10, pady=10)

        # String Check Frame
        check_frame = ttk.LabelFrame(self.master, text="String Parsing")
        check_frame.pack(padx=10, pady=10, fill=tk.X)

        # Input String
        input_frame = ttk.Frame(check_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(input_frame, text="Input String:").pack(side=tk.LEFT)
        self.input_entry = ttk.Entry(input_frame, width=40)
        self.input_entry.pack(side=tk.LEFT, padx=5)

        # Check String Button
        check_btn = ttk.Button(check_frame, text="Check String", command=self.check_string)
        check_btn.pack(padx=10, pady=10)

        # Results Frame
        results_frame = ttk.LabelFrame(self.master, text="Results")
        results_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Text Widget for Results
        self.results_text = tk.Text(results_frame, wrap=tk.WORD, height=15)
        self.results_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Scrollbar for Results
        scrollbar = ttk.Scrollbar(results_frame, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.configure(yscrollcommand=scrollbar.set)

    def define_grammar(self):
        # Reset the grammar
        self.grammar = Grammar()

        # Add S rules
        for entry in self.s_rules_entries:
            rule = entry.get().strip()
            if rule:
                self.grammar.add_rule("S", rule)

        # Add B rules
        for entry in self.b_rules_entries:
            rule = entry.get().strip()
            if rule:
                self.grammar.add_rule("B", rule)

        # Check if grammar is simple
        is_simple = self.grammar.is_simple()

        # Clear previous results
        self.results_text.delete(1.0, tk.END)

        # Display grammar simplicity
        self.results_text.insert(tk.END, f"Grammar Simplicity: {'Simple' if is_simple else 'Not Simple'}\n")

        if is_simple:
            messagebox.showinfo("Grammar", "The Grammar is Simple!")
        else:
            messagebox.showwarning("Grammar", "The Grammar is Not Simple!")

        # [Previous code remains the same, only the check_string method is updated]

    def check_string(self):
        # Check if grammar is defined
        if not hasattr(self, 'grammar') or not self.grammar.simple:
            messagebox.showerror("Error", "Please define a simple grammar first!")
            return

        input_string = self.input_entry.get().strip()
        if not input_string:
            messagebox.showerror("Error", "Please enter a string to parse!")
            return

        # Perform parsing
        parser = TopDownParser(self.grammar)
        is_accepted, parse_result, stack_after_checking = parser.check_string(input_string)

        # Clear previous results
        self.results_text.delete(1.0, tk.END)

        # Display parsing results
        self.results_text.insert(tk.END, f"The input string: {list(input_string)}\n")

        if is_accepted:
            self.results_text.insert(tk.END, "Parse Tree:\n")
            self.display_parse_tree(parse_result)
            self.results_text.insert(tk.END, "\nYour input string is Accepted.")
        else:
            self.results_text.insert(tk.END, "\nYour input string is Rejected.")

        # Always display the stack after checking
        self.results_text.insert(tk.END, f"\n\nThe stack after checking: {stack_after_checking}")

    # [Rest of the code remains the same]
    def display_parse_tree(self, node, indent="", is_last=True):
        # Use different connector for root vs. child nodes
        connector = "└── " if indent == "" else ("└── " if is_last else "├── ")
        self.results_text.insert(tk.END, f"{indent}{connector}{node['name']}\n")

        if 'children' in node and node['children']:
            for i, child in enumerate(node['children']):
                is_last_child = (i == len(node['children']) - 1)
                child_indent = indent + ("    " if is_last else "│   ")
                self.display_parse_tree(child, child_indent, is_last_child)


def main():
    root = tk.Tk()
    app = GrammarParserGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()