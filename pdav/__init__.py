from typing import Tuple
from io import StringIO

import numpy as np
import pandas as pd


def calculate_first_consecutive_indices(empty_indices):
    """
    empty_indices = [3,4,5,10,15,18,19,20,21,24]
    > [3, 10, 15, 18, 24]
    """
    actual_indices = []
    last_index = None
    for index in empty_indices:
        if not last_index:
            last_index = index
            actual_indices.append(last_index)
            continue
        if index == last_index+1:
            last_index=index
            continue
        else:
            last_index = index
            actual_indices.append(last_index) 
    return actual_indices


def lines_table_to_dataframe(lines, ignore_indices=[]) -> Tuple[pd.DataFrame,list[int]]:
    """
        ['Filesystem                             1K-blocks      Used  Available Use% Mounted on',
         '/dev/nvme1n1p2                         102131664  50899648   45997792  53% /',
         ...]
    """
    max_len = max(map(len, lines))

    array = np.array([[c for c in line.ljust(max_len)] for line in lines])

    empty_indices = [j for j,v in enumerate([(array[:,i]==' ').all() for i in range(max_len)]) if v]

    consecutive = calculate_first_consecutive_indices(empty_indices)
    if ignore_indices:
        for ii in sorted(ignore_indices, reverse=True):
            del consecutive[ii]
    for i in consecutive:
        array[:,i]='|'

    rows = [''.join(a) for a in array]
    text = '\n'.join(rows)
    sio = StringIO(text)
    sio.seek(0)
    df = pd.read_csv(sio, sep='|')
    df.columns = [c.strip() for c in df.columns]
    return df, consecutive


def text_to_df(text: str) -> pd.DataFrame:
    """
    improved version of lines_table_to_dataframe
    """
    lines = text.split('\n')
    max_len = max(map(len, lines))

    lines = [l.ljust(max_len) for l in lines]
    lines = [[c for c in line] for line in lines]
    array = np.array(lines)

    joined = None  # type: ignore
    for row in array==' ':
        if joined is None:
            joined = row
            continue
        joined &= row
    indices = []
    joined: np.ndarray
    for i, v in enumerate(joined):
        if v:
            indices.append(i)
    # print(indices)

    separate_indices = indices.copy()
    i = 0
    while i < len(separate_indices):
        # either shorten indices..
        if separate_indices[i-1]+1==separate_indices[i]:
            del separate_indices[i-1]
        # or increment i
        else:
            i += 1

    new_lines = []
    newer_lines = text.split('\n')
    rows = []
    full_indices = [0]+separate_indices+[None]
    for line in newer_lines:
        row = []
        for i,j in zip(full_indices, full_indices[1:]):
            row.append(line[i:j].strip())
        rows.append(row)

    df = pd.DataFrame(rows[1:], columns=rows[0])

    bools = (df=='').all().to_frame().reset_index().rename(columns={'index':'header',0:'bool'})
    merge_cols = bools.loc[lambda sdf: sdf['bool']].index.tolist()
    keep_cols = bools.loc[lambda sdf: ~sdf['bool']].index.tolist()

    new_df = df.copy()
    columns = new_df.columns.tolist()
    for i in merge_cols:
        columns[i+1] = columns[i]+' '+columns[i+1]
    new_df.columns = columns

    final_df = new_df.iloc[:,keep_cols]
    final_df = final_df.apply(pd.to_numeric, errors='ignore')
    return final_df
