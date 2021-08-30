from typing import Tuple


from token_ import Token


class Position:
    col = 0
    line = 0

    def get_values(self) -> Tuple[int]:
        pos = (self.line, self.col)
        return pos

    def update(self, char: str) -> True:
        if char != "start":
            self.col = self.col + 1 if char != "\n" else 0
            self.line = self.line if char != "\n" else self.line + 1

        return char != ""

