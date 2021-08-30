from typing import TextIO


from symbol_table import SymbolTable
from position import Position
from afd import AFD
from token_ import (
    RESERVED_WORDS,
    TOKEN_MAPPING,
    Token,
)


class Scanner:
    def __init__(self):
        self._afd = AFD()
        self._symb_table = SymbolTable(reserved_words=RESERVED_WORDS)
        self._pos = Position()

    def get_positions(self) -> tuple:
        return self._pos.get_values()

    def scanner(self, file: TextIO) -> Token:
        char = "start"
        lexeme = ""
        state = 0
        token_class = None

        while self._pos.update(char):
            char = file.read(1)

            state = self._afd.run(char, state)
            prev_token_class = token_class
            token_class = TOKEN_MAPPING.get(state)

            # print(self._pos.get_values(), repr(char), state, token_class)

            if prev_token_class != None and state == 0:
                token_class = prev_token_class
                file.seek(file.tell() - 1, 0)  # goes back one letter

                if lexeme in RESERVED_WORDS:
                    token_class = lexeme
                elif token_class == ["id"]:
                    token = self._symb_table.find(lexeme)

                if not (token_class == ["id"] and token != None):
                    token = Token(lexema=lexeme, classe=token_class)

                    if token_class == ["id"]:
                        self._symb_table.insert(token)

                return token
            elif not char in [" ", "\n", "\t"]:
                lexeme = lexeme + char

        return Token("$", "EOF")
