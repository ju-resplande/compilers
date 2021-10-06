import json
from typing import TextIO


import pandas as pd

from mgol.lexical.scanner import Scanner
from mgol.syntactic.recovery import PanicRecovery


class Parser:
    def __init__(self):
        self.stack = [0]
        self.scanner = Scanner()

        self.action = pd.read_table("srl_table/action.tsv")
        self.goto = pd.read_table("srl_table/goto.tsv")
        with open("srl_table/grammar.json") as f:
            self.grammar = json.load(f)

        self.recovery = PanicRecovery()

    def parse(self, file: TextIO):
        token = self.scanner.scan(file)

        while True:
            state = self.stack.pop()
            action_number = self.action[state][token.lemma]

            if pd.isnull(action_number):
                self.stack, self.scanner = self.recovery.recover(file, self.scanner)
                # imprimir onde ocorreu o erro e o tipo

            action, number = action_number
            if action == "s":
                self.stack.append(number)
                token = self.scanner.scan(file)
            elif action == "r":
                grammar_rule = self.grammar[number - 1]

                for _ in grammar_rule[1:]:
                    state = self.stack.pop()

                state = self.goto[state][self.grammar_rule[0]]
                self.stack.append(state)

                grammar_rule = grammar_rule[0] + " -> " + " ".join(grammar_rule[1:])
                print(grammar_rule)
            elif action == "a":
                break
