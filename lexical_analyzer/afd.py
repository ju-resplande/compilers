import string


class AFD:
    def _set_input(self, char: str) -> str:
        if char in string.digits:
            return "D"
        elif char in string.ascii_letters:
            return "L"
        elif char == ".":
            return "\."
        elif char in self._alphabet:
            return char
        else:
            return "ERRO"

    def run(self, char: str, state: int):
        char_input = self._set_input(char)
        if char_input == "ERRO":
            return 22
        elif char_input in self._transitions[state]:
            return self._transitions[state]

    _alphabet = {
        "D",
        "\.",
        "L",
        "e",
        "E",
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
        " ",
        "\t",
        "\n",
    }

    _transitions = {
        0: {
            "<": 1,
            "=": 3,
            ">": 4,
            "L": 5,
            "D": 6,
            "{": 11,
            '"': 13,
            "+": 16,
            "-": 16,
            "*": 16,
            "/": 16,
            "(": 17,
            ")": 18,
            ";": 19,
            ",": 20,
            "$": 21,
        },
        1: {"-": 2, "=": 3,},
        4: {"=": 3,},
        5: {"L": 5, "D": 5, "_": 5,},
        6: {"D": 6, "\.": 7, "e": 8, "E": 8,},
        7: {"D": 7, "e": 8, "E": 8,},
        8: {"+": 9, "-": 9, "D": 10,},
        9: {"D": 10,},
        10: {"D": 10,},
        11: {
            "}": 12,
            "{": 11,
            "D": 11,
            "\.": 11,
            "L": 11,
            "e": 11,
            "E": 11,
            "+": 11,
            "-": 11,
            "_": 11,
            "$": 11,
            "<": 11,
            ">": 11,
            "=": 11,
            "*": 11,
            "/": 11,
            ")": 11,
            "(": 11,
            ";": 11,
            ",": 11,
            '"': 11,
            " ": 11,
            "\t": 11,
            "\n": 11,
        },
        13: {
            '"': 14,
            "}": 13,
            "{": 13,
            "D": 13,
            "\.": 13,
            "L": 13,
            "e": 13,
            "E": 13,
            "+": 13,
            "-": 13,
            "_": 13,
            "$": 13,
            "<": 13,
            ">": 13,
            "=": 13,
            "*": 13,
            "/": 13,
            ")": 13,
            "(": 13,
            ";": 13,
            ",": 13,
            " ": 13,
            "\t": 13,
            "\n": 13,
        },
    }
