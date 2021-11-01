from typing import List


def print_error_msg(
    err_type: str, err_name: str, err_desc: str, scanner, prev_pos=False
):
    pos = scanner.get_positions(prev_pos=prev_pos)

    print(f"{err_type}: {err_name} - {err_desc}: linha {pos[0]}, coluna {pos[1]}",)


def grammar_rule_as_str(grammar_rule: List[str]):
    grammar_rule = grammar_rule[0] + " -> " + " ".join(grammar_rule[1:])

    return grammar_rule
