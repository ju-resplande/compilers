from typing import Set

from mgol.lexical.token_ import Token


class SymbolTable:
    def __init__(self, reserved_words: Set[str]):
        self._tokens: Set[Token] = {
            word: Token(lexema=word, classe=word, posicao=None)
            for word in reserved_words
        }

    def find(self, lexeme: str):
        return self._tokens.get(lexeme)

    def insert(self, token: Token):
        self._tokens.update({token.lexema: token})

