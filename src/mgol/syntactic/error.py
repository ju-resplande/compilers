import os

import pandas as pd


srl_table_path = os.path.join("srl_table", "srl.tsv")
srl_table = pd.read_table(srl_table_path)

action_columns = [c for c in srl_table.columns if c.islower() or c == "$"]
action_table = srl_table[action_columns]

error_numbers = action_table.isna().any(axis=1)
error_numbers = error_numbers[error_numbers].reset_index().drop(columns=[0])


def fill_error_num(row, error_numbers=error_numbers):
    for column in action_columns:
        if pd.isna(row[column]):
            row[column] = f"e{error_numbers.iloc[row.name]['index']+1}"

    return row


srl_table_err = srl_table.apply(fill_error_num, axis=1)

srl_table_err_path = os.path.join("srl_table", "srl_err.tsv")
srl_table_err.to_csv(srl_table_err_path, sep="\t", index=None)
