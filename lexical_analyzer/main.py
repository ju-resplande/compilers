from scanner import Scanner
from token_ import Token


def error(error_num: int, scanner: Scanner, token: Token):
    cur_pos = scanner.get_positions()
    token.classe = f"ERRO{error_num}"
    err_msg = f"ERRO{error_num} – Caractere inválido na linguagem, linha {cur_pos[0]}, coluna {cur_pos[1]}"
    print(err_msg)


def main():
    scanner = Scanner()

    error_num = 0
    with open("example.mgol") as f:
        while True:
            token = scanner.scanner(f)

            # if token.classe.startswith("ERRO"):
            #    error(error_num, scanner, token)
            #    error_num = error_num + 1

            print(token)

            if token.classe == "EOF":
                return


if __name__ == "__main__":
    main()
