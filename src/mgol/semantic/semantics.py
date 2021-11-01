import json
import os

from mgol.lexical.symbol_table import SymbolTable
from mgol.lexical.token_ import Token


class Semantics:
    _srl_dir = os.path.join(os.path.dirname(__file__), "..", "syntactic", "srl_table")

    with open(os.path.join(_srl_dir, "grammar.json")) as f:
        _grammar = json.load(f)

    def __init__(self, src_fname: str, symb_table: SymbolTable):
        self._src_fname = src_fname
        self._obj_fname = src_fname.replace(".mgol", ".c")
        self._obj_file = open(self._obj_fname, "w")
        self.imprimir = self._obj_file.write
        self.imprimir(self.HEADER)

        self._symb_table = symb_table

        # TODO: fechar arquivo objeto
        # TODO: atualizar escopo
        # TODO: lidar com erros

    def run(self, grammar_tokens, rule_number):
        if rule_number in self.NO_ACTION_RULES:
            pass
        if rule_number == 5:
            self.imprimir("\n\n\n")
        elif rule_number == 6:
            grammar_tokens["L"][0].tipo = grammar_tokens["TIPO"][0].tipo

            for token_lemma in grammar_tokens["L"][0].classe:
                token_found = self._symb_table.find(token_lemma)
                token_found.tipo = grammar_tokens["L"][0].tipo

            # print(self._symb_table._tokens)

            self.imprimir(";\n")
        elif rule_number == 7:
            grammar_tokens["L"][0].classe = grammar_tokens["L"][1].classe
            grammar_tokens["L"][0].classe.append(grammar_tokens["id"][0].lexema)

            self.imprimir(", " + grammar_tokens["id"][0].lexema)
        elif rule_number == 8:
            grammar_tokens["L"][0].classe.append(grammar_tokens["id"][0].lexema)

            self.imprimir(" " + grammar_tokens["id"][0].lexema)
        elif rule_number == 9:
            grammar_tokens["TIPO"][0].tipo = grammar_tokens["inteiro"][0].tipo
            self.imprimir(grammar_tokens["TIPO"][0].tipo)
        elif rule_number == 10:
            grammar_tokens["TIPO"][0].tipo = grammar_tokens["real"][0].tipo
            self.imprimir(grammar_tokens["TIPO"][0].tipo)
        elif rule_number == 11:
            grammar_tokens["TIPO"][0].tipo = grammar_tokens["literal"][0].tipo
            self.imprimir(grammar_tokens["TIPO"][0].tipo)
        elif rule_number == 13:
            print(self._symb_table._tokens)
            id_token = grammar_tokens["id"][0].lexema
            id_token = self._symb_table.find(id_token)

            # print(id_token)

        elif rule_number == 14:
            self.imprimir(f"print({grammar_tokens['ARG'][0].lexema});\n")
        elif rule_number == 15:
            pass
        elif rule_number == 16:
            pass
        elif rule_number == 17:
            pass
        elif rule_number == 19:
            pass
        elif rule_number == 20:
            pass
        elif rule_number == 21:
            pass
        elif rule_number == 22:
            pass
        elif rule_number == 23:
            pass
        elif rule_number == 25:
            self.imprimir("}\n")
        elif rule_number == 26:
            self.imprimir(f"if ({grammar_tokens['EXP_R'][0].lexema})" + "{\n")
        elif rule_number == 27:
            pass
        elif rule_number == 28:
            pass
        elif rule_number == 38:
            self.imprimir("}\n")

    HEADER = """#include <stdio.h>
typedef char literal[256];
typedef int inteiro;
typedef double real;

void main(void)
{
    """

    NO_ACTION_RULES = [
        1,
        2,
        3,
        4,
        12,
        18,
        24,
        28,
        29,
        30,
        31,
        32,
        34,
        35,
        36,
        37,
    ]
