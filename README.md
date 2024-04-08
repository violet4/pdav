# PDAV

Python Data Analysis and Visualization.

Making your data analysis workloads easier. Loading data from various sources more quickly.

## Convert a text table such as the output from `df` (linux disk free command):

```
Filesystem                             1K-blocks      Used  Available Use% Mounted on
/dev/sdb1                             2883128968 183795148 2552804212   7% /mnt/sabrent2
/dev/sda2                             2929993984 289155584 2640838400  10% /mnt/sabrent
192.168.2.16:/mnt/docker_drive/docker  719943752  36212876  647086220   6% /mnt/docker
...
```

Into a pandas dataframe:

```python
from pandas.api.types import is_numeric_dtype

from pdav import lines_table_to_dataframe

lines = subprocess.check_output(['df']).decode().strip('\n').split('\n')
df, _ = lines_table_to_dataframe(lines)

(
    df
    .assign(**{'Use%': lambda sdf: sdf['Use%'].str.replace('%','').astype(int)})
    .sort_values(by='Available', ascending=False)
    .apply(lambda ser: ser.map('{:,.0f}'.format) if is_numeric_dtype(ser) else ser)
    .head(3)
)
```

|    | Filesystem                            | 1K-blocks     | Used        | Available     |   Use% | Mounted on       |
|---:|:--------------------------------------|:--------------|:------------|:--------------|-------:|:-----------------|
| 12 | /dev/sda2                             | 2,929,993,984 | 289,155,584 | 2,640,838,400 |     10 | /mnt/sabrent     |
| 11 | /dev/sdb1                             | 2,883,128,968 | 183,795,148 | 2,552,804,212 |      7 | /mnt/sabrent2    |
| 13 | 192.168.2.16:/mnt/docker_drive/docker | 719,943,752   | 36,217,096  | 647,082,000   |      6 | /mnt/docker      |


## Handle datasets within zip files

```python
from pdav.dataset import DatasetZip

dsz = DatasetZip('/mnt/sabrent2/data/some_dataset.zip')
dsz.files
# [Dataset('/mnt/sabrent2/data/some_dataset.zip',
#          'home/sdf/sample_data.csv')]
df = dsz.files[0].to_frame()

df.iloc[:3,:3]
```

|    | Uniq Id                          | Product Name  |   Brand Name |
|---:|:---------------------------------|:--------------|-------------:|
|  0 | 4c69... | DB Longboards...                                        |          nan |
|  1 | 66d4... | Electronic Snap...                   |          nan |
|  2 | 2c55... | 3Doodler Create... |          nan |
