import string
from mgol.lexical.token_ import TOKEN_MAPPING
from mgol.lexical.error import error_state


class AFD:
    def _set_input(self, char: str) -> str:

        if char == "":
            return ""
        elif char in string.digits:
            return "D"
        elif char in string.ascii_letters:
            return "L"
        elif char == ".":
            return "\."
        elif char in self._alphabet:
            return char
        else:
            return "Invalid caracter"  # ERRO1

    def run(self, char: str, state: int):
        char_input = self._set_input(char)

        if char in {"e", "E"} and state in {6, 8}:
            return self._transitions[state][char]
        elif state in TOKEN_MAPPING and (
            not state in self._transitions or not char_input in self._transitions[state]
        ):
            return 0
        elif char_input in self._transitions[state]:
            # print(char, char_input, self._transitions[state][char_input])
            return self._transitions[state][char_input]
        else:
            return error_state(char_input, state)

    _alphabet = {
        "D",
        "\.",
        "L",
        "+",
        "-",
        "_",
        "$",
        "<",
        ">",
        "=",
        "*",
        "/",
        ")",
        "(",
        "{",
        "}",
        ";",
        ",",
        '"',
        "'",
        " ",
        "\t",
        "\n",
    }

    _transitions = {
        0: {
            "\n": 0,
            "\t": 0,
            " ": 0,
            "<": 1,
            "=": 3,
            ">": 4,
            "L": 5,
            "D": 6,
            "{": 12,
            '"': 14,
            "'": 16,
            "+": 19,
            "-": 19,
            "*": 19,
            "/": 19,
            "(": 20,
            ")": 21,
            ";": 22,
            ",": 23,
            "$": 24,
        },
        1: {"-": 2, "=": 3,},
        4: {"=": 3,},
        5: {"L": 5, "D": 5, "_": 5,},
        6: {"D": 6, "\.": 7, "e": 9, "E": 9,},
        7: {"D": 8},
        8: {"D": 8, "e": 9, "E": 9},
        9: {"+": 10, "-": 10, "D": 11,},
        10: {"D": 11,},
        11: {"D": 11,},
        12: {
            "}": 13,
            "{": 12,
            "D": 12,
            "\.": 12,
            "L": 12,
            "+": 12,
            "-": 12,
            "_": 12,
            "$": 12,
            "<": 12,
            ">": 12,
            "=": 12,
            "*": 12,
            "/": 12,
            ")": 12,
            "(": 12,
            ";": 12,
            ",": 12,
            '"': 12,
            "'": 12,
            " ": 12,
            "\t": 12,
            "\n": 12,
        },
        14: {
            '"': 15,
            "}": 14,
            "{": 14,
            "D": 14,
            "\.": 14,
            "L": 14,
            "+": 14,
            "-": 14,
            "_": 14,
            "$": 14,
            "<": 14,
            ">": 14,
            "=": 14,
            "*": 14,
            "/": 14,
            ")": 14,
            "(": 14,
            ";": 14,
            "'": 14,
            ",": 14,
            " ": 14,
            "'": 14,
            "\t": 14,
            "\n": 14,
        },
        16: {
            "'": 18,
            '"': 17,
            "}": 17,
            "{": 17,
            "D": 17,
            "\.": 17,
            "L": 17,
            "+": 17,
            "-": 17,
            "_": 17,
            "$": 17,
            "<": 17,
            ">": 17,
            "=": 17,
            "*": 17,
            "/": 17,
            ")": 17,
            "(": 17,
            ";": 17,
            ",": 17,
            " ": 17,
            "\t": 17,
            "\n": 17,
        },
        17: {"'": 15},
        18: {"'": 15},
    }
