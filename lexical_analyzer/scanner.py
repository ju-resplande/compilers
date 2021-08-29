from symbol_table import SymbolTable
from position import Position
from afd import AFD
from token_ import (
    RESERVED_WORDS,
    CLASS_MAPPING,
    INITIAL_STATE,
    Token,
)


class Scanner:
    def __init__(self):
        self._afd = AFD()
        self._symb_table = SymbolTable(reserved_words=RESERVED_WORDS)
        self._pos = Position()

    def get_positions(self) -> tuple:
        return self._pos.get_values()

    def _is_reserved_word(self, lexeme):
        return lexeme in RESERVED_WORDS

    def _is_space(self, char):
        return char in [" ", "\n", "\t"]

    def _found_token(self, prev_token_class, lexeme, char, state) -> bool:
        if lexeme == "":
            return False

        is_normal_token = prev_token_class != None and state == INITIAL_STATE

        return self._is_reserved_word(lexeme) or is_normal_token or self._is_space(char)

    def scanner(self, file) -> Token:
        char = "start"
        lexeme = ""
        state = 0
        token_class = None

        while self._pos.update(char):
            char = file.read(1)
            char = char if char != "" else "$"

            prev_state = state
            prev_token_class = token_class
            # print("prev_state", prev_state)
            # print("prev_token_class", prev_token_class)

            state = self._afd.run(char, state)
            token_class = CLASS_MAPPING.get(state)

            # print(self._pos.get_values(), repr(char), state, token_class)
            # print(self._found_token(prev_token_class, lexeme, char, state))

            if self._found_token(prev_token_class, lexeme, char, state):
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

                return token
            elif not self._is_space(char):
                lexeme = lexeme + char
