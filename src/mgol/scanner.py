import sys

from mgol.lexical.scanner import Scanner


def main():
    if len(sys.argv) < 1:
        raise ValueError("Usage: python scanner.py example1.mgol [--debug]")
    else:
        filename = sys.argv[1]

    to_debug = "--debug" in sys.argv
    scanner = Scanner(debug=to_debug)

    with open(filename) as f:
        while True:
            token = scanner.scan(f)

            if token.classe != "comentário":
                print(token)

            if token.classe == "EOF":
                return


if __name__ == "__main__":
    main()
