import pickle

def read_pickle(filename):
    with open(filename, 'rb') as fin:
        bin = fin.read()
    return pickle.loads(bin)

def write_pickle(filename, pickled):
    with open(filename, 'wb') as fout:
        fout.write(pickled)

def save_pickle(filename, var):
    write_pickle(filename, pickle.dumps(var))
