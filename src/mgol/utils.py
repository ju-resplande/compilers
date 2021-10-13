def print_error_msg(err_type: str, err_name: str, err_desc: str, scanner):
    cur_pos = scanner.get_positions()

    print(
        f"{err_type}: {err_name} - {err_desc}: linha {cur_pos[0]}, coluna {cur_pos[1]}",
    )
