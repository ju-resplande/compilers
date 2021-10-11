import sys

from mgol.lexical.error import ERROR_MAPPING
from mgol.lexical.scanner import Scanner


def main():
    if len(sys.argv) < 1:
        raise ValueError("Usage: python scanner.py example1.mgol")
    else:
        filename = sys.argv[1]

    scanner = Scanner()

    with open(filename) as f:
        while True:
            token = scanner.scan(f)

            if token.classe.startswith("ERRO"):
                cur_pos = scanner.get_positions()
                print(
                    f"{token.classe} - {ERROR_MAPPING[token.classe]}, linha {cur_pos[0]}, coluna {cur_pos[1]}"
                )

            if token.classe != "comentário":
                print(token)

            if token.classe == "EOF":
                break


if __name__ == "__main__":
    main()
