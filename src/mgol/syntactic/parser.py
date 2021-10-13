import os
import json
from typing import TextIO, List


import pandas as pd

from mgol.utils import print_error_msg
from mgol.lexical.scanner import Scanner


class Parser:
    _srl_dir = os.path.join(os.path.dirname(__file__), "srl_table")
    _srl = pd.read_table(os.path.join(_srl_dir, "srl_err.tsv"))
    _sync_symbols = [
        "inicio",
        "varinicio",
        "pt_v",
        "entao",
        "fimse",
        "fimrepita",
    ]

    with open(os.path.join(_srl_dir, "grammar.json")) as f:
        _grammar = json.load(f)

    _accept_rule = _grammar[0]

    def __init__(self, debug=False):
        self._stack = [0]
        self._scanner = Scanner()
        self._debug = debug
        self._sync_stack = [0]

    def _get_next_symbol(self, file: TextIO) -> str:
        while True:
            token = self._scanner.scan(file)

            if not token.classe.startswith("ERRO") and not token.classe.startswith(
                "comentário"
            ):
                break

        token_class = token.classe.lower()  # srl table uses only lowercase
        token_class = "$" if token_class == "eof" else token_class  # srl table uses $

        if self._debug:
            print(token)

        # if token.lexema == "m":
        #    exit()

        return token_class

    def _print_grammar_rule(self, grammar_rule: List[str]):
        grammar_rule = grammar_rule[0] + " -> " + " ".join(grammar_rule[1:])

        print(grammar_rule)

    def _print_error_msg(
        self, state: str, number: int, prev_token_class: str, token_class: str
    ):
        state_actions = self._srl.iloc[state]

        expected = state_actions[
            state_actions.str.contains(r"^r|s", regex=True, na=False)
        ].index.tolist()

        err_desc = (
            f'Esperava-se um token entre "{expected}" após {prev_token_class} \n'
            f'Mas recebeu "{token_class}" no lugar'
        )

        print_error_msg("Erro sintático", f"ERRO{number}", err_desc, self._scanner)

    def _recovery(self, token_class: str, file: TextIO):
        while True:
            token_class = self._get_next_symbol(file)

            if token_class in self._sync_symbols or token_class == "$":
                break

            # if token_class == "id":
            #    exit()

        if self._debug:
            print(f"sync_symbol: {token_class}")

        self._stack = self._sync_stack

        return token_class

    def parse(self, file: TextIO):
        token_class = self._get_next_symbol(file)
        prev_token_class = "o começo do programa"

        while True:
            state = self._stack[-1]

            if token_class in self._sync_symbols:
                self._sync_stack = self._stack.copy()

            if self._debug:
                print("\n")
                print(self._stack)
                print(f"Current State: {state}")

            action_number = self._srl[token_class][state]  # pandas column-oriented
            action, number = action_number[0], int(action_number[1:])

            if self._debug:
                print(
                    f'action: {"reduce" if action == "r" else "shift"} \n'
                    f"number: {number} \n"
                )

            if action == "e":
                self._print_error_msg(state, number, prev_token_class, token_class)
                token_class = self._recovery(token_class, file)

                if token_class == "$":
                    print_error_msg(
                        "Erro sintático",
                        "ERRO76",
                        "arquivo finalizado antes do esperado",
                        self._scanner,
                    )

                    return
            elif action == "s":
                self._stack.append(number)

                prev_token_class = token_class
                token_class = self._get_next_symbol(file)
            elif action == "r":
                grammar_rule = self._grammar[number - 1]

                if self._debug:
                    print(f"Rule: {number}")

                for _ in grammar_rule[1:]:
                    state = self._stack.pop()

                if self._debug:
                    print(self._stack)

                non_terminal = grammar_rule[0]
                state = self._stack[-1]

                if self._debug:
                    print(non_terminal)

                state = int(self._srl[non_terminal][state])
                # pandas column-oriented
                self._stack.append(state)

                self._print_grammar_rule(grammar_rule)
            if action == "a":
                self._print_grammar_rule(self._accept_rule)
                break
