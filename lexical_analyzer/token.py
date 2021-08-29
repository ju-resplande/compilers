from dataclasses import dataclass, field
from typing import Set, Dict


@dataclass
class Token:
    lexema: str
    classe: str = field(init=False)
    tipo: str

    def __post_init__(self):
        if self.classe == "NUM":
            self.tipo = "real" if "." in lexema else "inteiro"
        elif self.classe == "lit":
            self.tipo = "lit"
        elif self.classe == "id":
            self.tipo = "id"
        else:
            self.tipo = "NULO"

    def __repr__(self):
        return f"Classe: {self.classe}, Lexema: {self.lexema}, Tipo: {self.tipo}"


CLASS_MAPPING: Dict[int, str] = {
    2: "RCB",
    3: "OPR",
    5: "id",
    6: "NUM",
    7: "NUM",
    10: "Num",
    12: "comentário",
    14: "lit",
    16: "OPM",
    17: "AB_P",
    18: "FC_P",
    19: "PT_V",
    20: "Vir",
    21: "EOF",
    22: "ERRO",
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
