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


CLASS_MAPPING: Dict[int, str] = {
    1: "OPR",
    2: "RCB",
    3: "OPR",
    4: "OPR",
    5: "id",
    6: "NUM",
    7: "NUM",
    10: "NUM",
    12: "comentário",
    14: "lit",
    17: "OPM",
    18: "AB_P",
    19: "FC_P",
    20: "PT_V",
    21: "Vir",
    22: "EOF",
    23: "ERRO1",
    24: "ERRO2",
    25: "ERRO3",
    24: "ERRO4",
    25: "ERRO5",
    26: "ERRO6",
}

RESERVED_WORDS: Set[str] = {
    "inicio",
    "varinicio",
    "varfim",
    "escreva",
    "leia",
    "se",
    "entao",
    "fimse",
    "repita",
    "fimrepita",
    "fim",
    "inteiro",
    "literal",
    "real",
}
