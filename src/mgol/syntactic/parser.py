import re
import os
import json
from typing import TextIO, List


import pandas as pd

from mgol.lexical.scanner import Scanner
from mgol.syntactic.recovery import PanicRecovery


class Parser:
    def __init__(self, debug=False):
        self.stack = [0]
        self.scanner = Scanner()
        self.debug = debug

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
        token_class = "$" if token_class == "eof" else token_class  # srl table uses $

        return token_class, token  # for debug reasons

    def print_grammar_rule(self, grammar_rule: List[str]):
        grammar_rule = grammar_rule[0] + " -> " + " ".join(grammar_rule[1:])

        print(grammar_rule)

    def parse(self, file: TextIO):
        token_class, token = self.get_next_symbol(file)

        while True:
            state = self.stack[-1]

            if self.debug:
                print("\n")
                print(self.stack)
                print(f"Current State: {state}")

            action_number = self.action[token_class][state]  # pandas column-oriented

            if pd.isna(action_number):
                # imprimir onde ocorreu o erro e o tipo
                # erro pilha vazia? erro do scanner?
                self.stack, self.scanner = self.recovery.recover(file, self.scanner)
            else:
                action, number = action_number[0], int(action_number[1:])

                if self.debug:
                    print(f'action: {"reduce" if action == "r" else "shift"}')
                    print(f"nextState: {number}")
                    print(
                        f"token class: -{token.classe}- token lexema: -{token.lexema}- token tipo: -{token.tipo}-"
                    )

                if action == "s":
                    self.stack.append(number)
                    token_class, token = self.get_next_symbol(file)

                elif action == "r":
                    grammar_rule = self.grammar[number - 1]

                    if self.debug:
                        print(f"Rule: {number}")

                    for _ in grammar_rule[1:]:
                        state = self.stack.pop()

                    if self.debug:
                        print(self.stack)

                    non_terminal = grammar_rule[0]
                    state = self.stack[-1]

                    if self.debug:
                        print(non_terminal)

                    state = int(self.goto[non_terminal][state])
                    # pandas column-oriented
                    self.stack.append(state)

                    self.print_grammar_rule(grammar_rule)

                elif action == "a":
                    break
