import zipfile
from contextlib import contextmanager
from functools import wraps
from typing import Callable, Type

import pandas as pd

DataFrameFn = Callable[..., pd.DataFrame]


class Dataset:
    zip_path: str
    filename: str
    def __init__(self, zip_path:str, filename:str):
        self.zip_path = zip_path
        self.filename = filename

        self.read_csv: DataFrameFn = wraps(pd.read_csv)(self.wrap_read(pd.read_csv))
        self.read_tsv: DataFrameFn = wraps(pd.read_csv)(self.wrap_read(pd.read_csv, sep='\t'))
        self.read_excel: DataFrameFn = wraps(pd.read_excel)(self.wrap_read(pd.read_excel))

        self.read_clipboard: DataFrameFn = wraps(pd.read_clipboard)(self.wrap_read(pd.read_clipboard))
        self.read_fwf: DataFrameFn = wraps(pd.read_fwf)(self.wrap_read(pd.read_fwf))
        # self.read_hdf: DataFrameFn = wraps(pd.read_hdf)(self.wrap_read(pd.read_hdf))
        self.read_json: DataFrameFn = wraps(pd.read_json)(self.wrap_read(pd.read_json))
        self.read_parquet: DataFrameFn = wraps(pd.read_parquet)(self.wrap_read(pd.read_parquet))
        self.read_sas: DataFrameFn = wraps(pd.read_sas)(self.wrap_read(pd.read_sas))
        self.read_sql: DataFrameFn = wraps(pd.read_sql)(self.wrap_read(pd.read_sql))
        self.read_sql_table: DataFrameFn = wraps(pd.read_sql_table)(self.wrap_read(pd.read_sql_table))
        self.read_table: DataFrameFn = wraps(pd.read_table)(self.wrap_read(pd.read_table))
        self.read_feather: DataFrameFn = wraps(pd.read_feather)(self.wrap_read(pd.read_feather))
        self.read_gbq: DataFrameFn = wraps(pd.read_gbq)(self.wrap_read(pd.read_gbq))
        # self.read_html: DataFrameFn = wraps(pd.read_html)(self.wrap_read(pd.read_html))
        self.read_orc: DataFrameFn = wraps(pd.read_orc)(self.wrap_read(pd.read_orc))
        self.read_pickle: DataFrameFn = wraps(pd.read_pickle)(self.wrap_read(pd.read_pickle))
        self.read_spss: DataFrameFn = wraps(pd.read_spss)(self.wrap_read(pd.read_spss))
        self.read_sql_query: DataFrameFn = wraps(pd.read_sql_query)(self.wrap_read(pd.read_sql_query))
        self.read_stata: DataFrameFn = wraps(pd.read_stata)(self.wrap_read(pd.read_stata))
        self.read_xml: DataFrameFn = wraps(pd.read_xml)(self.wrap_read(pd.read_xml))

    def __repr__(self):
        return f"Dataset('{self.zip_path}', '{self.filename}')"

    @contextmanager
    def open(self):
        with zipfile.ZipFile(self.zip_path, 'r') as zf:
            with zf.open(self.filename) as fr:
                yield fr

    def wrap_read(self, fn: DataFrameFn, *args_base, **kwargs_base) -> DataFrameFn:
        @wraps(fn)
        def wrapped(*args_new, **kwargs_new) -> pd.DataFrame:
            with self.open() as fr:
                return fn(fr, *args_base, *args_new, **kwargs_base, **kwargs_new)
        return wrapped


class DatasetZip:
    files: list[Dataset]
    def __init__(self, zip_path, extensions=['.csv', '.xlsx', '.tsv']):
        self.extensions = extensions
        self.zip_path = zip_path
        self.files = self._load_datasets()

    def _load_datasets(self):
        datasets = []
        with zipfile.ZipFile(self.zip_path, 'r') as zf:
            for filename in zf.namelist():
                if filename.endswith(tuple(self.extensions)):
                    datasets.append(Dataset(self.zip_path, filename))
        return datasets

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.zip_path}')"
