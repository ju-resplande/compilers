from typing import Set

from mgol.lexical.token_ import Token


class SymbolTable:
    def __init__(self, reserved_words: Set[str]):
        self._tokens: Set[Token] = {
            Token(lexema=word, classe=word) for word in reserved_words
        }

    def find(self, lexeme: str):
        for token in self._tokens:
            if token.lexema == lexeme:
                return token

        return None

    def insert(self, token: Token):
        self._tokens.add(token)

    def update(self):
        raise NotImplementedError()

