import openpyxl
import pickle

def xlsx2bin(filename, config, output):
    rows, columns = config
    wb = openpyxl.load_workbook(filename)
    wsnames = wb.get_sheet_names()
    ws = wb.get_sheet_by_name(wsnames[0])
    raw_data = []
    for i in range(1, rows + 1):
        sample = []
        for j in range(1, columns + 1):
            sample.append(ws.cell(row=i, column=j).value)
        raw_data.append(sample)
        print('({0} / {1})...'.format(i, rows))
    pickled = pickle.dumps(raw_data)
    with open(output, 'wb') as fout:
        fout.write(pickled)
    print(filename + ' Done')

def main():
    # config = [filename, [rows, column], output]
    configs = [
        ['train_data.xlsx', [501, 8029], 'raw_data.bin'],
        ['test_a.xlsx', [101, 8028], 'test_a.bin'],
        ['test_b.xlsx', [121, 8028], 'test_b.bin'],
    ]
    for _ in configs:
        xlsx2bin(_[0], _[1], _[2])

if __name__ == '__main__':
    main()
