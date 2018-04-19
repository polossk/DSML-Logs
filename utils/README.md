# utils

most useful utils of data processing.

## `pickle_helper.py`

Providing some simple encapsulations of `pickle`.

* `read_pickle(filename)`: import pickle-ed binary file `filename` to python object
* `write_pickle(filename, pickled)`: save pickle-ed binary object `pickled` to file `filename`
* `save_pickle(filename, var)`: save python object `var` to file `filename`