from typing import List

from mgol.lexical.token_ import Token


def print_error_msg(err_type: str, err_name: str, err_desc: str, token: Token):

    print(
        f"{err_type}: {err_name} - {err_desc}: linha {token.posicao[0]}, coluna {token.posicao[1]}",
    )


def grammar_rule_as_str(grammar_rule: List[str]):
    grammar_rule = grammar_rule[0] + " -> " + " ".join(grammar_rule[1:])

    return grammar_rule
