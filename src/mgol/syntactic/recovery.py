from typing import TextIO

from mgol.lexical.scanner import Scanner


class PanicRecovery:
    sync_words = {")", "}", ";"}  # confirmar

    def recover(self, file: TextIO, scanner: Scanner):
        stack = [0]

        while scanner._pos.update("start", ""):
            char = file.read(1)

            if char in self.sync_words:
                break

        return stack, scanner
