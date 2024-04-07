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
lines = subprocess.check_output(['df']).decode().strip('\n').split('\n')
df, _ = lines_table_to_dataframe(lines)
df
```

|    | Filesystem                              |    1K-blocks |        Used |    Available | Use%   | Mounted on         |
|---:|:----------------------------------------|-------------:|------------:|-------------:|:-------|:-------------------|
|  0 | /dev/nvme1n1p2                          |    102131664 |    50899648 |     45997792 | 53%    | /                  |
|  1 | devtmpfs                                |         4096 |           0 |         4096 | 0%     | /dev               |
|  2 | tmpfs                                   |     32839468 |       86376 |     32753092 | 1%     | /dev/shm           |
|  3 | tmpfs                                   |     13135788 |       10560 |     13125228 | 1%     | /run               |
|  4 | tmpfs                                   |      8388608 |       17656 |      8370952 | 1%     | /tmp               |
|  5 | tmpfs                                   |      4194304 |           0 |      4194304 | 0%     | /var/tmp           |
|  6 | tmpfs                                   |     20971520 |           0 |     20971520 | 0%     | /var/tmp/portage   |
|  7 | /dev/nvme1n1p1                          |       497696 |      497696 |            0 | 100%   | /boot              |
|  8 | /dev/nvme1n1p3                          |    376388620 |   297533008 |     59662832 | 84%    | /home              |
|  9 | /dev/nvme2n1p1                          |    479591080 |   389356892 |     65798784 | 86%    | /mnt/stuff         |
| 10 | /dev/nvme0n1p1                          |    488146044 |   127048864 |    361097180 | 27%    | /mnt/monolith      |
| 11 | /dev/sdb1                               |   2883128968 |   183795148 |   2552804212 | 7%     | /mnt/sabrent2      |
| 12 | /dev/sda2                               |   2929993984 |   289155584 |   2640838400 | 10%    | /mnt/sabrent       |
| 13 | 192.168.2.16:/mnt/docker_drive/docker   |    719943752 |    36217096 |    647082000 | 6%     | /mnt/docker        |
| 14 | 192.168.2.25:home                       |    302776736 |   280278052 |     22379900 | 93%    | /mnt/synology      |
| 15 | tmpfs                                   |      6567892 |         120 |      6567772 | 1%     | /run/user/1000     |
