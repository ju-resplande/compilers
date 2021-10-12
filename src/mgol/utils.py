from typing import List


def print_error_msg(err_type: str, err_name: str, err_desc: str, cur_pos: List[int]):
    print(
        f"{err_type}: {err_name} - {err_desc}, linha {cur_pos[0]}, coluna {cur_pos[1]}",
    )
