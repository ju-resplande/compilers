from typing import Dict, List
import json
import os

from mgol.lexical.token_ import Token
from mgol.lexical.scanner import Scanner
from mgol.lexical.symbol_table import SymbolTable
from mgol.utils import print_error_msg


class Semantics:
    _srl_dir = os.path.join(os.path.dirname(__file__), "..", "syntactic", "srl_table")

    with open(os.path.join(_srl_dir, "grammar.json")) as f:
        _grammar = json.load(f)

    def __init__(
        self,
        src_fname: str,
        symb_table: SymbolTable,
        scanner: Scanner,
        stack: List[str],
    ):
        self._src_fname = src_fname
        self._obj_fname = src_fname.replace(".mgol", ".c")
        self._obj_file = open(self._obj_fname, "w")

        self._symb_table = symb_table
        self._scanner = scanner
        self._stack = stack

        self._imprimir(self._HEADER)

        self._ident = 1
        self._make_ident = lambda: self._ident * " " * 4
        self._temp_vars = []

        # TODO: testar erros

    def _copy_attrs(self, var1: Token, var2: Token):
        var2.classe = var1.classe
        var2.lexema = var1.lexema
        var2.tipo = var1.tipo

    def _make_temp_declarations(self):
        with open(self._obj_fname) as f:
            obj_string = f.read()

        idx = obj_string.find(self._TEMP_HEADER) + len(self._TEMP_HEADER)

        temp_var_declaration = "\n"
        for temp_idx, temp_var_type in enumerate(self._temp_vars):
            temp_var_declaration += f"    {temp_var_type} T{temp_idx}; \n"

        temp_var_declaration += "    /*-----------------------------*/\n"

        obj_string = obj_string[:idx] + temp_var_declaration + obj_string[idx:]

        with open(self._obj_fname, "w") as f:
            f.write(obj_string)

    def _imprimir(self, text: str):
        loop_token = None

        for token in reversed(self._stack):
            if token.classe == "repita":
                loop_token = token
                break

        if loop_token:
            if loop_token.lexema == "repita":
                loop_token.lexema = list()

            loop_token.lexema.append(text)
        else:
            self._obj_file.write(text)

    def run(self, grammar_tokens: Dict[str, Token], rule_number: int):
        if rule_number in self._NO_ACTION_RULES:
            pass
        elif rule_number == 2:
            self._imprimir("}\n")
            self._obj_file.close()
            self._make_temp_declarations()
        elif rule_number == 5:
            self._imprimir("\n\n\n")
        elif rule_number == 6:
            grammar_tokens["L"][0].tipo = grammar_tokens["TIPO"][0].tipo

            for token_lemma in grammar_tokens["L"][0].classe:
                token_found = self._symb_table.find(token_lemma)
                token_found.tipo = grammar_tokens["L"][0].tipo

            self._imprimir(";\n")
        elif rule_number == 7:
            grammar_tokens["L"][0].classe = grammar_tokens["L"][1].classe
            grammar_tokens["L"][0].classe.append(grammar_tokens["id"][0].lexema)

            self._imprimir(", " + grammar_tokens["id"][0].lexema)
        elif rule_number == 8:
            grammar_tokens["L"][0].classe.append(grammar_tokens["id"][0].lexema)

            self._imprimir(" " + grammar_tokens["id"][0].lexema)
        elif rule_number == 9:
            grammar_tokens["TIPO"][0].tipo = grammar_tokens["inteiro"][0].tipo
            self._imprimir(self._make_ident() + grammar_tokens["TIPO"][0].tipo)
        elif rule_number == 10:
            grammar_tokens["TIPO"][0].tipo = grammar_tokens["real"][0].tipo
            self._imprimir(self._make_ident() + grammar_tokens["TIPO"][0].tipo)
        elif rule_number == 11:
            grammar_tokens["TIPO"][0].tipo = grammar_tokens["literal"][0].tipo
            self._imprimir(self._make_ident() + grammar_tokens["TIPO"][0].tipo)
        elif rule_number == 13:
            id_token = grammar_tokens["id"][0].lexema
            id_token = self._symb_table.find(id_token)

            if id_token.tipo == "literal":
                self._imprimir(
                    self._make_ident() + f'scanf("%s", {id_token.lexema});\n'
                )
            elif id_token.tipo == "inteiro":
                self._imprimir(
                    self._make_ident() + f'scanf("%d", &{id_token.lexema});\n'
                )
            elif id_token.tipo == "real":
                self._imprimir(
                    self._make_ident() + f'scanf("%lf", &{id_token.lexema});\n'
                )
            else:
                print_error_msg(
                    "Erro semântico",
                    "ERRO1",
                    f"variável {id_token.lexema} não declarada",
                    self._scanner,
                )
                exit()

        elif rule_number == 14:
            self._imprimir(
                self._make_ident() + f"print({grammar_tokens['ARG'][0].lexema});\n"
            )
        elif rule_number == 15:
            self._copy_attrs(grammar_tokens["lit"][0], grammar_tokens["ARG"][0])
        elif rule_number == 16:
            self._copy_attrs(grammar_tokens["num"][0], grammar_tokens["ARG"][0])
        elif rule_number == 17:
            id_token = grammar_tokens["id"][0].lexema
            id_token = self._symb_table.find(id_token)

            if id_token.tipo == "NULO":
                print_error_msg(
                    "Erro semântico",
                    "ERRO1",
                    f"variável {id_token.lexema} não declarada",
                    self._scanner,
                )
                exit()

            self._copy_attrs(id_token, grammar_tokens["ARG"][0])
        elif rule_number == 19:
            id_token = grammar_tokens["id"][0].lexema
            id_token = self._symb_table.find(id_token)

            if id_token.tipo == "NULO":
                print_error_msg(
                    "Erro semântico",
                    "ERRO1",
                    f"variável {id_token.lexema} não declarada",
                    self._scanner,
                )
                exit()
            elif grammar_tokens["LD"][0].tipo != grammar_tokens["id"][0].tipo:
                print_error_msg(
                    "Erro semântico",
                    "ERRO4",
                    "Tipos diferentes para atribuição",
                    self._scanner,
                )

                exit()

            attribution = (
                self._make_ident()
                + id_token.lexema
                + " "
                + grammar_tokens["rcb"][0].lexema.replace("<-", "=")
                + " "
                + grammar_tokens["LD"][0].lexema
                + ";\n"
            )

            self._imprimir(attribution)
        elif rule_number == 20:
            if grammar_tokens["OPRD"][0].tipo != grammar_tokens["OPRD"][1].tipo:
                print_error_msg(
                    "Erro semântico",
                    "ERRO2",
                    "operandos"
                    f"{grammar_tokens['OPRD'][0].lexema} e {grammar_tokens['OPRD'][1].lexema}",
                    "com tipos incompatíveis",
                    self._scanner,
                )
                exit()
            elif grammar_tokens["OPRD"][0].tipo == "literal":
                print_error_msg(
                    "Erro semântico",
                    "ERRO3",
                    "operandos não podem ser literais",
                    self._scanner,
                )
                exit()

            tx_lexema = (
                grammar_tokens["OPRD"][1].lexema
                + " "
                + grammar_tokens["opm"][0].lexema
                + " "
                + grammar_tokens["OPRD"][0].lexema
            )

            tx_name = f"T{len(self._temp_vars)}"

            self._temp_vars.append(grammar_tokens["OPRD"][0].tipo)
            self._imprimir(self._make_ident() + tx_name + " = " + tx_lexema + ";\n")
            grammar_tokens["LD"][0].lexema = tx_name
            grammar_tokens["LD"][0].tipo = grammar_tokens["OPRD"][0].tipo

        elif rule_number == 21:
            self._copy_attrs(grammar_tokens["OPRD"][0], grammar_tokens["LD"][0])
        elif rule_number == 22:
            id_token = grammar_tokens["id"][0].lexema
            id_token = self._symb_table.find(id_token)

            if id_token.tipo == "NULO":
                print_error_msg(
                    "Erro semântico",
                    "ERRO1",
                    f"variável {id_token.lexema} não declarada",
                    self._scanner,
                )
                exit()
            else:
                self._copy_attrs(id_token, grammar_tokens["OPRD"][0])
        elif rule_number == 23:
            self._copy_attrs(grammar_tokens["num"][0], grammar_tokens["OPRD"][0])
        elif rule_number == 25:
            self._ident -= 1
            self._imprimir(self._make_ident() + "}\n")
        elif rule_number == 26:
            self._imprimir(
                self._make_ident() + f"if ({grammar_tokens['EXP_R'][0].lexema})" + "{\n"
            )

            self._ident += 1
        elif rule_number == 27:
            if grammar_tokens["OPRD"][0].tipo != grammar_tokens["OPRD"][1].tipo:
                print_error_msg(
                    "Erro semântico",
                    "ERRO2",
                    "operandos"
                    f"{grammar_tokens['OPRD'][0].lexema} e {grammar_tokens['OPRD'][1].lexema}",
                    "com tipos incompatíveis",
                    self._scanner,
                )
                exit()

            tx_lexema = (
                grammar_tokens["OPRD"][1].lexema
                + " "
                + grammar_tokens["opr"][0].lexema
                + " "
                + grammar_tokens["OPRD"][0].lexema
            )

            tx_name = f"T{len(self._temp_vars)}"

            self._temp_vars.append(grammar_tokens["OPRD"][0].tipo)
            self._imprimir(self._make_ident() + tx_name + " = " + tx_lexema + ";\n")
            grammar_tokens["EXP_R"][0].lexema = tx_name
        elif rule_number == 33:
            tx_name = grammar_tokens["EXP_R"][0].lexema

            cmds = grammar_tokens["repita"][0].lexema
            cond_loop = cmds[0]

            self._imprimir(cond_loop)
            self._imprimir(self._make_ident() + f"while ({tx_name})" + "{\n")

            for cmd in cmds[1:]:
                self._imprimir("    " + cmd)

            self._imprimir("    " + cond_loop)

            self._imprimir(self._make_ident() + "}\n")

    _TEMP_HEADER = "    /*----Variaveis temporarias----*/"

    _HEADER = (
        """#include <stdio.h>
typedef char literal[256];
typedef int inteiro;
typedef double real;

void main(void)
{
"""
        + _TEMP_HEADER
    )

    _NO_ACTION_RULES = [
        1,
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
