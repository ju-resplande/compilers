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
        self.recovery = PanicRecovery()

    def parse(self, file: TextIO):
        token = self.scanner.scan(file)

        while True:
            state = self.stack.pop()
            action, state = self.action[state][token.lemma]

            if action == "shift":
                self.stack.append(state)
                token = self.scanner.scan(file)
            elif action == "reduce":
                # desempilha os simbolos
                self.stack.append(t)  # quem é o t??
                state = self.goto[t][A]  # quem é a??
                self.stack.append(state)
                # imprimir regra que foi reduzida
            elif action == "accept":
                break
            else:
                self.recovery.recover()
                # imprimir onde ocorreu o erro e o tipo
