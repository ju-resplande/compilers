import sys

from mgol.syntactic.parser import Parser


def main():
    if len(sys.argv) < 1:
        raise ValueError("Usage: python parser.py example1.mgol [--debug]")
    else:
        filename = sys.argv[1]

    to_debug = "--debug" in sys.argv
    parser = Parser(debug=to_debug)

    with open(filename) as f:
        parser.parse(f)


if __name__ == "__main__":
    main()
