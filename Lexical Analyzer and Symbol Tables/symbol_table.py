from typing import Set

from token import Token

class SymbolTable:
    _tokens: Set[Token]

    def __init__(self, tokens: Set[Token]):
        self._tokens = tokens

    def find(lexeme: str):
        for token in _self.tokens:
            if token.lexema == lexeme:
                return token

        return None
        

    def insert(self, token: Token):
        self._tokens.add(token)
    
    def update(self):
        pass # TODO: implementar