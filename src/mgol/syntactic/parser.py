import os
import json
from typing import TextIO, List


import pandas as pd

from mgol.lexical.token_ import Token
from mgol.utils import print_error_msg
from mgol.lexical.scanner import Scanner
from mgol.syntactic.recovery import PanicRecovery


class Parser:
    def __init__(self, debug=False):
        self.stack = [0]
        self.scanner = Scanner()
        self.debug = debug

        srl_dir = os.path.join(os.path.dirname(__file__), "srl_table")

        srl_table = os.path.join(srl_dir, "srl_err.tsv")
        self.action = self.goto = pd.read_table(srl_table)  # readability

        grammar_file = os.path.join(srl_dir, "grammar.json")
        with open(grammar_file) as f:
            self.grammar = json.load(f)

        self.accept_rule = self.grammar[0]

        self.recovery = PanicRecovery()

    def get_next_symbol(self, file: TextIO) -> str:
        while True:
            token = self.scanner.scan(file)
            if not token.classe.startswith("ERRO"):
                break

        token_class = token.classe.lower()  # srl table uses only lowercase
        token_class = "$" if token_class == "eof" else token_class  # srl table uses $

        return token_class, token  # for debug and error_msg reasons

    def print_grammar_rule(self, grammar_rule: List[str]):
        grammar_rule = grammar_rule[0] + " -> " + " ".join(grammar_rule[1:])

        print(grammar_rule)

    def print_error_msg(self, state: str, number: int, prev_token: Token):
        state_actions = self.action.iloc[state]

        expected = state_actions[
            state_actions.str.contains(r"^r|s", regex=True, na=False)
        ].index.tolist()

        print(expected)

        # map symbol names?

        cur_pos = self.scanner.get_positions()
        err_desc = f"Esperados as palavras {expected} após {prev_token}"
        print_error_msg(
            "Erro sintático", f"ERRO{number}", err_desc, cur_pos,
        )

    def parse(self, file: TextIO):
        token_class, token = self.get_next_symbol(file)
        prev_token = "o começo do programa"

        while True:
            state = self.stack[-1]

            if self.debug:
                print("\n")
                print(self.stack)
                print(f"Current State: {state}")

            action_number = self.action[token_class][state]  # pandas column-oriented
            action, number = action_number[0], int(action_number[1:])

            if self.debug:
                print(f'action: {"reduce" if action == "r" else "shift"}')
                print(f"number: {number}")
                print(
                    f"token class: -{token.classe}- token lexema: -{token.lexema}- token tipo: -{token.tipo}-"
                )

            if action == "e":
                self.print_error_msg(state, number, prev_token)
                self.stack, self.scanner = self.recovery.recover(file, self.scanner)
            elif action == "s":
                self.stack.append(number)

                prev_token = token
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
                self.print_grammar_rule(self.accept_rule)
                break
