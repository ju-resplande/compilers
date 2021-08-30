from typing import Dict

ERROR_MAPPING: Dict[str, str] = {
    "ERRO1": "Caractere inválido na linguagem",
    "ERRO2": "Numeral não pode ser finalizado com '.'",
    "ERRO3": "Numeral não pode ser finalizado com 'e' ou 'E'",
    "ERRO4": "Numeral não pode ser finalizado com '+' ou '-'",
    "ERRO5": "Comentário deve ser finalizado com '}'",
    "ERRO6": "'' inválido na linguagem",
    "ERRO7": "Literal deve ser finalizado com \" ou ' ",
    "ERRO8": "Erro desconhecido no reconhecimento do token",
}


def error_state(char_input: str, state: str) -> int:
    if char_input == "Invalid caracter":
        return 24
    elif state == 7:
        return 25
    elif state == 9:
        return 26
    elif state == 10:
        return 27
    elif state == 12:
        return 28
    elif state in 15 and char_input == "'":
        return 29
    elif state == [14, 16]:
        return 30
    else:
        return 31
