import os
import unittest
import subprocess

from pdav import lines_table_to_dataframe
from pdav.dataset import DatasetZip

this_dir = os.path.dirname(os.path.abspath(__file__))

class TestLinesTableToDataframe(unittest.TestCase):

    def test_lines_table_to_dataframe(self):
        print("\nRead command line `df` output:")
        lines = subprocess.check_output(['df']).decode().strip('\n').split('\n')
        df, _ = lines_table_to_dataframe(lines)
        df = df.assign(**{'Use%': lambda sdf: sdf['Use%'].str.replace('%','').astype(int)}).sort_values(by='Use%',ascending=False)
        print(df.head().to_markdown())
        if 'Available' in df.columns:
            print('Total Available:', df['Available'].sum())

    def test_read_zip(self):
        print("\nRead from within zip:")
        dz = DatasetZip(os.path.join(this_dir, 'sample.zip'))
        print(dz)
        print(dz.files)
        df = dz.files[0].read_csv()
        print(df.to_markdown())
