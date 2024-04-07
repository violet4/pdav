import unittest
import subprocess

from pdav import lines_table_to_dataframe

class TestLinesTableToDataframe(unittest.TestCase):
    def test_lines_table_to_dataframe(self):
        lines = subprocess.check_output(['df']).decode().strip('\n').split('\n')
        df, _ = lines_table_to_dataframe(lines)
        df = df.assign(**{'Use%': lambda sdf: sdf['Use%'].str.replace('%','').astype(int)}).sort_values(by='Use%',ascending=False)
        print(df)
        if 'Available' in df.columns:
            print('Total Available:', df['Available'].sum())
