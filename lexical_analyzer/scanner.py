from symbol_table import SymbolTable
from position import Position
from afd import AFD
from token_ import (
    RESERVED_WORDS,
    CLASS_MAPPING,
    ERROR_STATE,
    Token,
)


class Scanner:
    def __init__(self):
        self._afd = AFD
        self._symb_table = SymbolTable(reserved_words=RESERVED_WORDS)
        self._pos = Position()

    def get_positions(self) -> tuple:
        return self._pos.get_values()

    def _is_reserved_word(self, lexeme):
        return lexeme in RESERVED_WORDS

    def _found_token(self, prev_token_class, lexeme, char, state) -> bool:
        is_normal_token = prev_token_class != None and state == ERROR_STATE
        is_space = char in [" ", "\n", "\t"]

        return self._is_reserved_word(lexeme) or is_normal_token or is_space

    def scanner(self, file) -> Token:
        char = "start"
        lexeme = ""
        state = 0
        token_class = None

        while self._pos.update(char):
            char = file.read(1) if char != "" else "$"

            prev_state = state
            prev_token_class = token_class

            state = self._afd.run(char, state)
            token_class = CLASS_MAPPING.get(state)

            if self._found_token(self, prev_token_class, state, lexeme):
                if not self._is_reserved_word(lexeme):  # found in previous position
                    state = prev_state
                    token_class = prev_token_class
                    file.seek(file.tell() - 1, 0)  # goes back one letter

                if token_class == ["id"]:
                    token = self._symb_table.find(lexeme)

                if not (token_class == ["id"] and token != None):
                    token = Token(lexema=lexeme, classe=token_class)

                    if token_class == ["id"]:
                        self._symb_table.insert(token)
            else:
                lexeme = lexeme + char
