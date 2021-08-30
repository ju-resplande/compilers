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
    18: "OPM",
    19: "AB_P",
    20: "FC_P",
    21: "PT_V",
    22: "Vir",
    23: "EOF",
    24: "ERRO1",
    25: "ERRO2",
    26: "ERRO3",
    27: "ERRO4",
    28: "ERRO5",
    29: "ERRO6",
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
