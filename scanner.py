import sys

from mgol.lexical.scanner import Scanner


def main():
    if len(sys.argv) < 1:
        raise ValueError("Usage: python scanner.py example1.mgol")
    else:
        filename = sys.argv[1]

    scanner = Scanner()

    with open(filename) as f:
        token = scanner.scan(f)

        while token.classe != "EOF":
            if token.classe != "comentário":
                print(token)

            token = scanner.scan(f)


if __name__ == "__main__":
    main()
