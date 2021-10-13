def print_error_msg(
    err_type: str, err_name: str, err_desc: str, scanner, prev_pos=False
):
    pos = scanner.get_positions(prev_pos=prev_pos)

    print(f"{err_type}: {err_name} - {err_desc}: linha {pos[0]}, coluna {pos[1]}",)
