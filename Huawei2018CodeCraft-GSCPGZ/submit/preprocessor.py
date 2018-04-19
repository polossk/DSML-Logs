# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
import scanner

STD_TIME_FMT = '%Y-%m-%d %H:%M:%S'

class SolidServer(object):
    def __init__(self, cpu, mem, disk):
        self.cpu = cpu
        self.mem = mem * 1024
        self.disk = disk

class Flavor(object):
    def __init__(self, flavorID, cpu, mem):
        self.flavorID = int(flavorID[6:])
        self.cpu = cpu
        self.mem = mem
        self.name = flavorID

class TrainingSet(object):
    def __init__(self, trainData, inputFile):
        self.trainData = trainData
        self.inputFile = inputFile
        self.flavor_dick = {'flavor1': [1.0, 1024.0],
                            'flavor2': [1.0, 2048.0],
                            'flavor3': [1.0, 4096.0],
                            'flavor4': [2.0, 2048.0],
                            'flavor5': [2.0, 4096.0],
                            'flavor6': [2.0, 8192.0],
                            'flavor7': [4.0, 4096.0],
                            'flavor8': [4.0, 8192.0],
                            'flavor9': [4.0, 16384.0],
                            'flavor10': [8.0, 8192.0],
                            'flavor11': [8.0, 16384.0],
                            'flavor12': [8.0, 32768.0],
                            'flavor13': [16.0, 16384.0],
                            'flavor14': [16.0, 32768.0],
                            'flavor15': [16.0, 65536.0]}

        fr = open(inputFile)
        # read server data
        server = fr.readline().strip().split()
        self.server = SolidServer(float(server[0]), float(server[1]), float(server[2]))
        fr.readline()
        self.flvNum = int(fr.readline())
        # read flavor data
        self.flavors = []
        while True:
            hoge = fr.readline()
            if hoge[0] == 'f':
                temp = hoge.strip().split()
                temp_flavor = Flavor(temp[0], float(temp[1]), float(temp[2]))
                self.flavors.append(temp_flavor)
            else:
                break

        # read optimization object
        opt = fr.readline().strip()
        self.opt = opt
        fr.readline()

        # read time interval
        start = fr.readline().strip()
        end = fr.readline().strip()
        self.startTime = datetime.strptime(start, STD_TIME_FMT).date()
        self.endTime = datetime.strptime(end, STD_TIME_FMT).date()
        self.lenTime = (self.endTime - self.startTime).days
        fr.close()

        frTrain = open(trainData)
        self.trainTime = datetime.strptime(frTrain.readline().strip().split('\t')[2],
                                           STD_TIME_FMT).date()
        frTrain.close()
        self.raw_train_data = scanner.scanner(trainData)

    def get_flavorID(self):
        res = []
        for hoge in self.flavors:
            res.append(hoge.flavorID)
        return res

    def moving_windows(self, start, end, data, preEnd=None):
        train_X, train_y = [], []
        if preEnd == None:
            for hoge in data:
                yy, mm, dd = hoge[2:]
                time = datetime(yy, mm, dd).date()
                if time >= start and time < end:
                    train_X.append(hoge)
            return train_X
        for hoge in data:
            yy, mm, dd = hoge[2:]
            time = datetime(yy, mm, dd).date()
            if time >= start and time < end:
                train_X.append(hoge)
            elif time >= end and time < preEnd:
                train_y.append(hoge)
        return train_X, train_y

    def getWin_TrainData(self):
        train_X, train_y = [], []
        fr = open(self.trainData)
        all_data = self.raw_train_data
        begin = self.trainTime
        test_begin = self.startTime - timedelta(days=self.lenTime*2)
        while begin < self.startTime:
            end = begin + timedelta(days=self.lenTime*2)
            preEnd = end + timedelta(days=self.lenTime)
            if preEnd < self.startTime:
                res = self.moving_windows(begin, end, all_data, preEnd)
                train_X.append(res[0])
                train_y.append(res[1])
            begin += timedelta(days=1)
        test_X = self.moving_windows(test_begin, self.startTime, all_data)
        return train_X, train_y, test_X

    def process_feat(self, k):
        sample = [0] * 21
        yy, mm, dd = k[-1][2:]
        end = datetime(yy, mm, dd).date()
        for hoge in k:
            flavor = hoge[1]
            if flavor not in self.flavor_dick.keys():
                continue
            yy, mm, dd = hoge[2:]
            date = datetime(yy, mm, dd).date()
            if (date >= end - timedelta(days=7)):
                sample[18] += 1.0
                sample[19] += self.flavor_dick[flavor][0]
                sample[20] += self.flavor_dick[flavor][1]
            sample[2] += 1
            id = int(flavor[6:])
            sample[0] += self.flavor_dick[flavor][0]
            sample[1] += self.flavor_dick[flavor][1]
            sample[2 + id] += 1.0
        return sample

    def getTrainFeat(self):
        train_X, train_y, test_X = self.getWin_TrainData()
        featName = ['n_cpu', 'n_mem', 'n_flavors',
                    'fla1', 'fla2', 'fla3', 'fla4', 'fla5', 'fla6', 'fla7', 'fla8',
                    'fla9', 'fla10' 'fla11', 'fla12', 'fla13', 'fla14', 'fla15',
                    'last_flavors', 'last_cpu', 'last_mem']
        feat_X = []
        feat_y = []
        for k in train_X:
            feat_X.append(self.process_feat(k))
        feat_test_X = self.process_feat(test_X)
        for k in train_y:
            sample = [0] * 15
            for hoge in k:
                flavor = hoge[1]
                id = int(flavor[6:])
                if id > 15: continue
                sample[id - 1] += 1
            feat_y.append(sample)
        return feat_X, feat_y, feat_test_X


if __name__ == '__main__':
    makeTrain = TrainingSet('TrainData_2015.1.1_2015.2.19.txt',
                            'input_5flavors_cpu_7days.txt')
    feat_X, feat_y, test_feat = makeTrain.getTrainFeat()
    i = 0
    for hoge in feat_X:
        print(i, hoge)
        i += 1
    print(test_feat)
