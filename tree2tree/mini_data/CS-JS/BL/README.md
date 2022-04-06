# Data

The data in this folder is extracted from the author's original dataset.
As the original data is too large to be uploaded on github and run on my own computer,
I extracted the first few objects from the original one.

| data  | Origin size | Mini data |
| ----- | ----------- | --------- |
| train | 100000      | 100       |
| test  | 10000       | 10        |
| valid | 10000       | 10        |

| parm                | Origin size | Mini data |
| ------------------- | ----------- | --------- |
| train obj           | 1000000     | 100       |
| Num of epoch        | 30          | 1         |
| batch size          | 100         | 10        |
| step per checkpoint | 500         | 10        |

# Script

The code to split the original data is in this repo/utils/dataset_splitter.py
