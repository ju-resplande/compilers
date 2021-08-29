from typing import Dict

ERROR_MAPPING: Dict[str, str]] = {
    "ERRO1": "Caractere inválido na linguagem",
    "ERRO2": "Numeral não pode ser finalizado com 'e' ou 'E'",
    "ERRO3": "Numeral não pode ser finalizado com '+' ou '-'",
    "ERRO4": "Comentário deve ser finalizado com '}'",
    "ERRO5": "Literal deve ser finalizado com \" ou ' ",
    "ERRO6": "'' inválido na linguagem",
    "ERRO7": "Erro desconhecido no reconhecimento do token",
}

def error_state(char: str, state: str) -> str:
    if char == "-1":
        return "ERRO1"
    elif state == 8:
        return "ERRO2"
    elif state == 9:
        return "ERRO3"
    elif state == 11:
        return "ERRO4"
    elif state in [13, 16]:
        return "ERRO5"
    elif state == 15:
        return "ERRO6"
    else:
        return "ERRO7"