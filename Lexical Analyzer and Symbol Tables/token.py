from dataclasses import dataclass
from enum import Enum, auto

@dataclass
class Token:
    lexema: str
    classe: str
    tipo: str


RESERVED_WORDS = {
    Token(lexema='inicio', classe='inicio', tipo='NULO'),
    Token(lexema='varinicio', classe='varinicio', tipo='NULO'),
    Token(lexema='varfim', classe='varfim', tipo='NULO'),
    Token(lexema='escreva', classe='escreva', tipo='NULO'),
    Token(lexema='leia', classe='leia', tipo='NULO'),
    Token(lexema='se', classe='se', tipo='NULO'),
    Token(lexema='entao', classe='entao', tipo='NULO'),
    Token(lexema='fimse', classe='fimse', tipo='NULO'),
    Token(lexema='repita', classe='repita', tipo='NULO'),
    Token(lexema='fimrepita', classe='fimrepita', tipo='NULO'),
    Token(lexema='fim', classe='fim', tipo='NULO'),
    Token(lexema='inteiro', classe='inteiro', tipo='inteiro'),
    Token(lexema='literal', classe='literal', tipo='literal'),
    Token(lexema='real', classe='real', tipo='real'),
}