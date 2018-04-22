import pandas as pd
from .csv_helper import *
from .pickle_helper import *

def icolumn_chars(x, length, begin_char):
    a = [0] * length
    a[ord(x) - ord(begin_char)] = 1
    return a

def icolumn_nums(x, length, begin_num):
    a = [0] * length
    a[(x) - (begin_num)] = 1
    return a

def column_B(x): return icolumn_chars(x, 6, 'J')

def column_HY(x):
    return [0, 1] if x == 'A' else [1, 0]

def column_ABY(x):
    return [0, 1] if x == 'E' else [1, 0]

def column_ACU(x): return icolumn_chars(x, 3, 'C')

def column_AJJ(x):
    return [0, 1] if x == 'E0' else [1, 0]

def column_BMM(x):
    d = {206:1, 215:2, 329:3, 530:4, 1018:5, 1110:6, 1113:7, 1245:8, 2823:9}
    return icolumn_nums(d[x], 9, 1)

def column_CMQ(x): return icolumn_chars(x, 3, 'A')


def column_ELC(x):
    d = {2409:1, 3009:2, 4106:3, 4147:4}
    return icolumn_nums(d[x], 4, 1)


def column_ESU(x): return icolumn_chars(x, 9, 'P')


def column_FDJ(x): return icolumn_chars(x, 3, 'B')


def column_HUY(x):
    return [0, 1] if x == 'XY1' else [1, 0]


def column_IDE(x): return icolumn_nums(x, 15, 1)


def column_IRX(x):
    return [0, 1] if x == 'A' else [1, 0]

def column_ZZZ(x): return x


def hcolumn_B():
    return ['TOOL_ID_' + str(_) for _ in range(6)]

def hcolumn_HY():
    return ['Tool_' + str(_) for _ in range(2)]

def hcolumn_ABY():
    return ['TOOL_ID (#1)_' + str(_) for _ in range(2)]

def hcolumn_ACU():
    return ['TOOL_ID (#2)_' + str(_) for _ in range(3)]

def hcolumn_AJJ():
    return ['TOOL_ID (#3)_' + str(_) for _ in range(2)]

def hcolumn_BMM():
    return ['Tool (#1)_' + str(_) for _ in range(9)]

def hcolumn_CMQ():
    return ['Tool (#2)_' + str(_) for _ in range(3)]

def hcolumn_ELC():
    return ['tool_' + str(_) for _ in range(4)]

def hcolumn_ESU():
    return ['tool (#1)_' + str(_) for _ in range(9)]

def hcolumn_FDJ():
    return ['TOOL_' + str(_) for _ in range(3)]

def hcolumn_HUY():
    return ['TOOL (#1)_' + str(_) for _ in range(2)]

def hcolumn_IDE():
    return ['Tool (#3)_' + str(_) for _ in range(15)]

def hcolumn_IRX():
    return ['TOOL (#2)_' + str(_) for _ in range(2)]

def hcolumn_ZZZ():
    return ['' + str(_) for _ in range(1)]

def onehot(raw_data, output):
    idx = [2, 233, 753, 775, 946, 1703, 2383,
           3695, 3895, 4170, 5979, 6193, 6576, 0]
    fidx = [column_B, column_HY, column_ABY, column_ACU, 
            column_AJJ, column_BMM, column_CMQ, column_ELC,
            column_ESU, column_FDJ, column_HUY, column_IDE,
            column_IRX, column_ZZZ]
    hidx = [hcolumn_B, hcolumn_HY, hcolumn_ABY, hcolumn_ACU, 
            hcolumn_AJJ, hcolumn_BMM, hcolumn_CMQ, hcolumn_ELC,
            hcolumn_ESU, hcolumn_FDJ, hcolumn_HUY, hcolumn_IDE,
            hcolumn_IRX, hcolumn_ZZZ]
    raw_data = read_pickle(raw_data)

    _h, _, _1, _2 = raw_data[0], [], [], []
    j, length, rows = 0, len(_h), len(raw_data)
    for i in range(1, length):
        if i + 1 == idx[j]:
            _1.extend(hidx[j]())
            j += 1
        else:
            _1.append(_h[i])
    for e in range(1, rows):
        j, sample, _3 = 0, raw_data[e], []
        for i in range(1, length):
            if i + 1 == idx[j]:
                _3.extend(fidx[j](sample[i]))
                j += 1
            else:
                _3.append(sample[i])
        _.append(_3)
        _2.append(sample[0])
        print('({0} / {1})...'.format(e, rows))

    pddf = pd.DataFrame(_, columns=_1, index=_2)
    pickled = pickle.dumps(pddf)
    write_pickle('{0}.dataframe.bin'.format(output), pickled)
    print('Job Done.')