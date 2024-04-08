Convert a text table such as the output from `df` (linux disk free command):

```
Filesystem                             1K-blocks      Used  Available Use% Mounted on
/dev/nvme1n1p2                         102131664  50899648   45997792  53% /
devtmpfs                                    4096         0       4096   0% /dev
tmpfs                                   32839468     86376   32753092   1% /dev/shm
tmpfs                                   13135788     10560   13125228   1% /run
tmpfs                                    8388608     17656    8370952   1% /tmp
tmpfs                                    4194304         0    4194304   0% /var/tmp
tmpfs                                   20971520         0   20971520   0% /var/tmp/portage
/dev/nvme1n1p1                            497696    497696          0 100% /boot
/dev/nvme1n1p3                         376388620 297531432   59664408  84% /home
/dev/nvme2n1p1                         479591080 389356892   65798784  86% /mnt/stuff
/dev/nvme0n1p1                         488146044 127048864  361097180  27% /mnt/monolith
/dev/sdb1                             2883128968 183795148 2552804212   7% /mnt/sabrent2
/dev/sda2                             2929993984 289155584 2640838400  10% /mnt/sabrent
192.168.2.16:/mnt/docker_drive/docker  719943752  36212876  647086220   6% /mnt/docker
192.168.2.25:home                      302776736 280278052   22379900  93% /mnt/synology
tmpfs                                    6567892       120    6567772   1% /run/user/1000
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
)
```

|    | Filesystem                            | 1K-blocks     | Used        | Available     |   Use% | Mounted on       |
|---:|:--------------------------------------|:--------------|:------------|:--------------|-------:|:-----------------|
| 12 | /dev/sda2                             | 2,929,993,984 | 289,155,584 | 2,640,838,400 |     10 | /mnt/sabrent     |
| 11 | /dev/sdb1                             | 2,883,128,968 | 183,795,148 | 2,552,804,212 |      7 | /mnt/sabrent2    |
| 13 | 192.168.2.16:/mnt/docker_drive/docker | 719,943,752   | 36,217,096  | 647,082,000   |      6 | /mnt/docker      |
| 10 | /dev/nvme0n1p1                        | 488,146,044   | 127,048,864 | 361,097,180   |     27 | /mnt/monolith    |
|  9 | /dev/nvme2n1p1                        | 479,591,080   | 389,356,892 | 65,798,784    |     86 | /mnt/stuff       |
|  8 | /dev/nvme1n1p3                        | 376,388,620   | 297,533,008 | 59,662,832    |     84 | /home            |
|  0 | /dev/nvme1n1p2                        | 102,131,664   | 50,899,648  | 45,997,792    |     53 | /                |
|  2 | tmpfs                                 | 32,839,468    | 86,376      | 32,753,092    |      1 | /dev/shm         |
| 14 | 192.168.2.25:home                     | 302,776,736   | 280,278,052 | 22,379,900    |     93 | /mnt/synology    |
|  6 | tmpfs                                 | 20,971,520    | 0           | 20,971,520    |      0 | /var/tmp/portage |
|  3 | tmpfs                                 | 13,135,788    | 10,560      | 13,125,228    |      1 | /run             |
|  4 | tmpfs                                 | 8,388,608     | 17,656      | 8,370,952     |      1 | /tmp             |
| 15 | tmpfs                                 | 6,567,892     | 120         | 6,567,772     |      1 | /run/user/1000   |
|  5 | tmpfs                                 | 4,194,304     | 0           | 4,194,304     |      0 | /var/tmp         |
|  1 | devtmpfs                              | 4,096         | 0           | 4,096         |      0 | /dev             |
|  7 | /dev/nvme1n1p1                        | 497,696       | 497,696     | 0             |    100 | /boot            |
