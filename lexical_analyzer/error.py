from typing import Dict

ERROR_MAPPING: Dict[str, str] = {
    "ERRO1": "Caractere inválido na linguagem",
    "ERRO2": "Numeral não pode ser finalizado com '.'",
    "ERRO3": "Numeral não pode ser finalizado com 'e' ou 'E'",
    "ERRO4": "Numeral não pode ser finalizado com '+' ou '-'",
    "ERRO5": "Comentário deve ser finalizado com '}'",
    "ERRO6": "Literal deve ser finalizado com \" ou ' ",
    "ERRO7": "Literal '' inválido",
    "ERRO8": "Erro desconhecido no reconhecimento do token",
}


def error_state(char_input: str, state: int) -> int:
    if char_input == "Invalid caracter":
        return 25
    elif state == 7:
        return 26
    elif state == 9:
        return 27
    elif state == 10:
        return 28
    elif state == 12:
        return 29
    elif state in [14, 17]:
        return 30
    elif state == 18:
        return 31
    else:
        return 32
