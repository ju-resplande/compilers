from error import ERROR_MAPPING
from scanner import Scanner


def main():
    scanner = Scanner()

    with open("example.mgol") as f:
        while True:
            token = scanner.scanner(f)

            if token.classe.startswith("ERRO"):
                cur_pos = scanner.get_positions()
                print(
                    f"{token.classe} - {ERROR_MAPPING[token.classe]}, linha {cur_pos[0]}, coluna {cur_pos[1]}"
                )

            print(token)

            if token.classe == "EOF":
                return


if __name__ == "__main__":
    main()
