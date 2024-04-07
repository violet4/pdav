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
    max_len

    array = np.array([[c for c in line.ljust(max_len)] for line in lines])

    empty_indices = [j for j,v in enumerate([(array[:,i]==' ').all() for i in range(max_len)]) if v]

    consecutive = calculate_first_consecutive_indices(empty_indices)
    if ignore_indices:
        for ii in ignore_indices:
            consecutive.remove(ii)
    for i in consecutive:
        array[:,i]='|'

    rows = [''.join(a) for a in array]
    text = '\n'.join(rows)
    sio = StringIO(text)
    sio.seek(0)
    df = pd.read_csv(sio, sep='|')
    df.columns = [c.strip() for c in df.columns]
    return df, consecutive
