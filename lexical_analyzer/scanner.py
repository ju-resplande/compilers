

from symbol_table import SymbolTable
from position import Position
from afd import AFD
from token import (
    RESERVED_WORDS,
    CLASS_MAPPING,
    Token,
)


class Scanner:
    def __init__(self):
        self._afd = AFD
        self._symb_table = SymbolTable(reserved_words=RESERVED_WORDS)
        self._pos = Position()
    
    def get_positions() -> tuple:
        return self._pos.get_values()

    def scanner(self, file) -> Token:
        state = 0
        lexeme = ''
        char = 'start'

        while self._pos.update():
            char = file.read(1) if char != '' else '$'

            state = self._afd.run(char, state)
            token_class = CLASS_MAPPING.get(state)

            if token_class == None and not lexeme in RESERVED_WORDS:
                lexeme = lexeme + char
            else:
                if token_class == ['id']:
                    token = self.symb_table.find(lexeme)

                if not (token_class == ['id'] and token != None):
                    token = Token(lexema=lexeme, classe=token_class)
                
                    if token_class == ['id']:
                        self.symb_table.insert(token)

                return token