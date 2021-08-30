from dataclasses import dataclass, field
from typing import Set, Dict


@dataclass(unsafe_hash=True)
class Token:
    lexema: str = field(hash=True)
    classe: str
    tipo: str = field(init=False)

    def __post_init__(self):
        if self.classe == "NUM":
            self.tipo = "real" if "." in self.lexema else "inteiro"
        elif self.classe == "lit":
            self.tipo = "lit"
        elif self.classe == "id":
            self.tipo = "id"
        else:
            self.tipo = "NULO"

    def __repr__(self):
        return f"Classe: {self.classe}, Lexema: {self.lexema}, Tipo: {self.tipo}"


TOKEN_MAPPING: Dict[int, str] = {
    1: "OPR",
    2: "RCB",
    3: "OPR",
    4: "OPR",
    5: "id",
    6: "NUM",
    8: "NUM",
    11: "NUM",
    13: "comentário",
    15: "lit",
    19: "OPM",
    20: "AB_P",
    21: "FC_P",
    22: "PT_V",
    23: "Vir",
    24: "EOF",
    25: "ERRO1",
    26: "ERRO2",
    27: "ERRO3",
    28: "ERRO4",
    29: "ERRO5",
    30: "ERRO6",
    31: "ERRO7",
    32: "ERRO8",
}

RESERVED_WORDS: Set[str] = {
    "entao",
    "escreva",
    "fim",
    "fimrepita",
    "fimse",
    "inicio",
    "inteiro",
    "leia",
    "literal",
    "real",
    "repita",
    "se",
    "varinicio",
    "varfim",
}
