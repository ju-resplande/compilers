from typing import TextIO


from mgol.lexical.symbol_table import SymbolTable
from mgol.lexical.error import ERROR_MAPPING
from mgol.lexical.position import Position
from mgol.lexical.afd import AFD
from mgol.lexical.token_ import (
    RESERVED_WORDS,
    TOKEN_MAPPING,
    Token,
)
from mgol.utils import print_error_msg


class Scanner:
    _afd = AFD()
    symb_table = SymbolTable(reserved_words=RESERVED_WORDS)

    def __init__(self, debug=False):
        self._pos = Position()
        self._debug = debug

    def get_positions(self, prev_pos) -> tuple:
        return self._pos.get_values(prev_pos)

    def scan(self, file: TextIO) -> Token:
        char = "start"
        state = 0
        lexeme = ""
        token = None
        token_class = None

        while self._pos.update(char, lexeme):
            char = file.read(1) if char != "" else "$"

            if self._debug:
                print(f"state: {state}")
                print(f"lexeme: {lexeme}")
                print(self.get_positions(prev_pos=False), repr(char))

            state = self._afd.run(char, state)
            prev_token_class = token_class
            token_class = TOKEN_MAPPING.get(state)

            if prev_token_class != None and state == 0:
                token_class = prev_token_class
                file.seek(file.tell() - 1, 0)  # goes back one letter

                if lexeme in RESERVED_WORDS:
                    token_class = lexeme
                elif token_class == "id":
                    token = self.symb_table.find(lexeme)

                if not (token_class == "id" and token != None):
                    token = Token(
                        lexema=lexeme,
                        classe=token_class,
                        posicao=self.get_positions(prev_pos=True),
                    )

                    if token_class == "id":
                        self.symb_table.insert(token)

                if token.classe.startswith("ERRO"):
                    print_error_msg(
                        "Erro léxico", token.classe, ERROR_MAPPING[token.classe], token,
                    )

                return token
            elif not (char in [" ", "\n", "\t"] and not lexeme.startswith('"')):
                lexeme = lexeme + char

        return Token("$", "EOF", None)
