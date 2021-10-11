import sys

from mgol.syntactic.parser import Parser


def main():
    if len(sys.argv) < 1:
        raise ValueError("Usage: python main.py example1.mgol")
    else:
        filename = sys.argv[1]

    parser = Parser()

    with open(filename) as f:
        parser.parse(f)


if __name__ == "__main__":
    main()
