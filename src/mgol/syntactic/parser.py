import os
import json
from typing import TextIO
from pprint import pprint


import pandas as pd

from mgol.utils import print_error_msg, grammar_rule_as_str
from mgol.lexical.scanner import Scanner
from mgol.lexical.token_ import Token
from mgol.semantic.semantics import Semantics


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

    def __init__(self, filename: str, debug: bool = False):
        self._filename = filename
        self._debug = debug

        self._stack = dict()
        self._stack["semantic"] = []
        self._stack["sync_semantic"] = []

        self._stack["syntactic"] = [0]
        self._stack["sync_syntactic"] = [0]

        self._scanner = Scanner()
        self._semantics = Semantics(
            src_fname=self._filename,
            symb_table=self._scanner.symb_table,
            scanner=self._scanner,
        )

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

        return token_class, token

    def _print_error_msg(
        self,
        state: str,
        number: int,
        prev_token_class: str,
        token_class: str,
        token: Token,
    ):
        state_actions = self._srl.iloc[state]

        expected = state_actions[
            state_actions.str.contains(r"^r|s", regex=True, na=False)
        ].index.tolist()

        err_desc = (
            f'Esperava-se um token entre "{expected}" após {prev_token_class} \n'
            f'Mas recebeu "{token_class}" no lugar'
        )

        print_error_msg("Erro sintático", f"ERRO{number}", err_desc, token)

    def _recovery(self, token_class: str, file: TextIO):
        while True:
            token_class, token = self._get_next_symbol(file)

            if token_class in self._sync_symbols or token_class in ["$", "fim"]:
                break

        if self._debug:
            print(f"sync_symbol: {token_class}")

        self._stack["syntactic"] = self._stack["sync_syntactic"]

        return token_class, token

    def parse(self, file: TextIO):
        token_class, token = self._get_next_symbol(file)

        prev_token_class = "o começo do programa"

        while True:
            state = self._stack["syntactic"][-1]

            if token_class in self._sync_symbols:
                self._stack["sync_syntactic"] = self._stack["syntactic"].copy()
                self._stack["sync_semantic"] = self._stack["semantic"].copy()

            if self._debug:
                print("\n")
                print(self._stack["syntactic"])
                pprint(self._stack["semantic"])
                print(f"Current State: {state}")

            action_number = self._srl[token_class][state]  # pandas column-oriented
            action, number = action_number[0], int(action_number[1:])

            if self._debug:
                print(
                    f'action: {"reduce" if action == "r" else "shift"} \n'
                    f"number: {number} \n"
                )

            if action == "e":
                self._print_error_msg(
                    state, number, prev_token_class, token_class, token
                )

                token_class, token = self._recovery(token_class, file)

                if token_class in ["$", "fim"]:
                    print_error_msg(
                        "Erro sintático",
                        "ERRO76",
                        "arquivo finalizado antes do esperado",
                        token,
                    )

                    return
            elif action == "s":
                self._stack["syntactic"].append(number)

                prev_token_class = token_class

                self._stack["semantic"].append(token)
                if token.classe == "repita":
                    self._semantics._loop_stack.append(token)

                token_class, token = self._get_next_symbol(file)
            elif action == "r":
                grammar_rule = self._grammar[number - 1]

                if self._debug:
                    print(f"Rule: {number}")

                non_terminal = grammar_rule[0]
                non_terminal_token = Token(
                    lexema=non_terminal, classe=[], posicao=token.posicao
                )

                grammar_tokens = dict()
                grammar_tokens[non_terminal] = [non_terminal_token]
                for token_name in reversed(grammar_rule[1:]):
                    self._stack["syntactic"].pop()
                    grammar_token = self._stack["semantic"].pop()

                    if grammar_token.classe == "repita":
                        self._semantics._loop_stack.pop()

                    if token_name not in grammar_tokens:
                        grammar_tokens[token_name] = list()

                    grammar_tokens[token_name].append(grammar_token)

                if self._debug:
                    print(self._stack["syntactic"])
                    pprint(self._stack["semantic"])

                state = self._stack["syntactic"][-1]

                self._semantics.run(grammar_tokens, number)

                if self._debug:
                    print(non_terminal_token)

                state = int(self._srl[non_terminal][state])

                # pandas column-oriented
                self._stack["syntactic"].append(state)
                self._stack["semantic"].append(non_terminal_token)

            if action in ["a", "r"]:
                grammar_rule = grammar_rule if action == "r" else self._accept_rule

                if self._debug:
                    print(grammar_rule_as_str(grammar_rule))

            if action == "a":
                break
