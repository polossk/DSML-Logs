import sys
sys.path.append('../')
from utils.csv_helper import *
from utils.xslx_helper import *
from utils.pickle_helper import *

def main():
    idics_ABC = [
        'A', 'B', 'HY', 'ABY', 'ACU', 'AJJ', 'BMM', 'CMQ',
        'ELC', 'ESU', 'FDJ', 'HUY', 'IDE', 'IRX', 'KVU'
    ]
    works = ['raw_data.bin', 'test_a.bin', 'test_b.bin']
    idics = list(map(abc2dec, idics_ABC))
    for _ in works:
        if _ != 'raw_data.bin': idx = idics[:-1]
        raw_data = read_pickle(_)
        load = lambda a, x: a[x]
        string_data = []
        for sample in raw_data:
            def load_help(x): return load(sample, x - 1)
            string_data.append(list(map(load_help, idx)))
        print(string_data[-1])
        print(len(string_data[-1]))
        pickled = pickle.dumps(string_data)
        write_pickle('string_'+_, pickled)
        write_csv('string_{0}.csv'.format(_), string_data)

if __name__ == '__main__':
    main()
