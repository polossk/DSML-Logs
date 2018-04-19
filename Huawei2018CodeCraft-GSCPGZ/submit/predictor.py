# -*- coding: utf-8 -*-
import preprocessor
import regTree
import scanner

class SolidServer(object):
    def __init__(self, config):
        self.rest_cpu = config.cpu
        self.rest_mem = config.mem
        self.haveFlavors = {}

    def addVM(self, flavor):
        # add one virtual machine
        if flavor in self.haveFlavors.keys():
            self.haveFlavors[flavor] += 1
        else:
            self.haveFlavors[flavor] = 1
        self.rest_cpu -= flavor.cpu
        self.rest_mem -= flavor.mem

    def validate(self, flavor):
        # if rest resources is fit for new vm
        return self.rest_cpu >= flavor.cpu and self.rest_mem >= flavor.mem


def predict_vm(ecsDataPath, inputFilePath):
    result = []

    raw = preprocessor.TrainingSet(ecsDataPath, inputFilePath)

    test_flavor = raw.get_flavorID()
    pred = []
    train_X, train_y, test_feat = raw.getTrainFeat()
    for hoge in test_flavor:
        train_flavorID = regTree.makeFlavorTrain(hoge - 1, train_X, train_y)
        temp_regTree = regTree.build(train_flavorID)
        pred.append(round(regTree.predict(temp_regTree, test_feat)))

    flavors, server = raw.flavors, raw.server
    box = [SolidServer(server)]

    i = raw.flvNum - 1
    while i >= 0:
        temp_flavor = flavors[i]
        temp_pred = pred[i]
        while temp_pred > 0:
            j = 0
            while j < len(box):
                if box[j].validate(temp_flavor):
                    box[j].addVM(temp_flavor)
                    break
                else:
                    j += 1
            if j == len(box):
                tmp = SolidServer(raw.server)
                tmp.addVM(temp_flavor)
                box.append(tmp)
            temp_pred -= 1
        i -= 1

    res = sum(pred)
    result.append(str(int(res)) + '\n')
    for k in range(raw.flvNum):
        msg = 'flavor{0} {1}\n'.format(str(test_flavor[k]), int(pred[k]))
        result.append(msg)
    result.append('\n' + str(len(box)) + '\n')
    for x in range(len(box)):
        result.append(str(x + 1))
        for key in box[x].haveFlavors.keys():
            msg = ' {0} {1}'.format(key.name, str(box[x].haveFlavors[key]))
            result.append(msg)
        if x < len(box) - 1:
            result.append('\n')

    return result
