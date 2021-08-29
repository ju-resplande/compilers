from typing import Tuple


class Position:
    col = 0
    line = 0

    def get_values(self) -> Tuple[int]:
        pos = (self.line, self.col)
        return pos

    def update(self, char: str):
        if char == "start":
            return

        self.col = self.col + 1 if char != "\n" else 0
        self.line = self.line if char != "\n" else self.line + 1

