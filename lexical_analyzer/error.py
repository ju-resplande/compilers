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


def error_state(char: str, state: str) -> str:
    if char == "-1":
        return "ERRO1"
    elif state == 7:
        return "ERRO2"
    elif state == 9:
        return "ERRO3"
    elif state == 10:
        return "ERRO4"
    elif state == 12:
        return "ERRO5"
    elif state in 15 and char == "'":
        return "ERRO6"
    elif state == [14, 16]:
        return "ERRO7"
    else:
        return "ERRO8"
