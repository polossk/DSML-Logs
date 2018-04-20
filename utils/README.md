# utils

most useful utils of data processing.

## `csv_helper.py`

Providing some simple tools of processing csv file

* `write_csv(filename, data_table)`: write a `data_table` to csv file, where `data_table` formatted in `[[], [], ...]`

## `pickle_helper.py`

Providing some simple encapsulations of `pickle`.

* `read_pickle(filename)`: import pickle-ed binary file `filename` to python object
* `write_pickle(filename, pickled)`: save pickle-ed binary object `pickled` to file `filename`
* `save_pickle(filename, var)`: save python object `var` to file `filename`