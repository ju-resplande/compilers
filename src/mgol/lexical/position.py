from typing import List


class Position:
    def __init__(self) -> None:
        self._cur_pos = [1, 1]
        self._prev_pos = [1, 1]

    def get_values(self, prev_pos) -> List[int]:
        pos = self._cur_pos if not prev_pos else self._prev_pos

        return pos

    def update(self, char: str, lexeme: str) -> bool:
        self._prev_pos = self._cur_pos.copy()

        if char != "start":
            self._cur_pos[0] = (
                self._cur_pos[0] if char != "\n" else self._cur_pos[0] + 1
            )
            self._cur_pos[1] = self._cur_pos[1] + 1 if char != "\n" else 1

        return lexeme != "" or char != ""

