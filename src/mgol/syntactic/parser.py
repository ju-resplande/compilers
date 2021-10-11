import re
import os
import json
from typing import TextIO, List


import pandas as pd

from mgol.lexical.scanner import Scanner
from mgol.syntactic.recovery import PanicRecovery


class Parser:
    def __init__(self):
        self.stack = [0]
        self.scanner = Scanner()

        srl_dir = os.path.join(os.path.dirname(__file__), "srl_table")

        srl_table = os.path.join(srl_dir, "srl.tsv")
        self.action = self.goto = pd.read_table(srl_table)

        grammar_file = os.path.join(srl_dir, "grammar.json")
        with open(grammar_file) as f:
            self.grammar = json.load(f)

        self.recovery = PanicRecovery()

    def get_next_symbol(self, file: TextIO) -> str:
        token = self.scanner.scan(file)
        token_class = token.classe.lower()  # srl table uses only lowercase

        print(f"Lendo: {token_class}, {token.lexema}")

        return token_class

    def print_grammar_rule(self, grammar_rule: List[str]):
        grammar_rule = grammar_rule[0] + " -> " + " ".join(grammar_rule[1:])
        print(grammar_rule)

    def parse(self, file: TextIO):
        token_class = self.get_next_symbol(file)

        while True:
            state = self.stack[-1]

            print("-" * 30)

            action_number = self.action[token_class][state]  # pandas column-oriented
            action, number = action_number[0], int(action_number[1:])

            print(f"action: {action, number}")
            print(f"stack: {self.stack}")

            if action == "s":
                self.stack.append(number)
                token_class = self.get_next_symbol(file)

            elif action == "r":
                grammar_rule = self.grammar[number - 1]

                for _ in grammar_rule[1:]:
                    state = self.stack.pop()

                non_terminal = grammar_rule[0]
                state = self.stack[-1]
                print(non_terminal, state)

                state = int(self.goto[non_terminal][state])  # pandas column-oriented
                self.stack.append(state)

                self.print_grammar_rule(grammar_rule)

            elif action == "a":
                break
            elif action == "e":
                # imprimir onde ocorreu o erro e o tipo
                # erro pilha vazia? erro do scanner?
                self.stack, self.scanner = self.recovery.recover(file, self.scanner)
