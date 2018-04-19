# -*- coding: utf-8 -*-
import preprocessor
import copy

def binSplitDataSet(DataSet, feature, value):
    mat0 = []
    mat1 = []
    for hoge in DataSet:
        if hoge[feature] > value:
            mat0.append(hoge)
        else:
            mat1.append(hoge)
    return mat0, mat1

def regLeaf(dataSet):
    sum = 0.0
    for hoge in dataSet:
        sum += hoge[-1]
    return sum / len(dataSet)

def regErr(dataSet):
    err = 0.0
    mean = regLeaf(dataSet)
    for hoge in dataSet:
        err += (hoge[-1] - mean) * (hoge[-1] - mean)
    return err

def isSameVal(dataSet):
    res = set()
    for hoge in dataSet:
        res.add(hoge[-1])
    if len(res) == 1:
        return True
    else:
        return False

def getFeatSet(dataSet, feat):
    res = set()
    for hoge in dataSet:
        res.add(hoge[feat])
    return res

def chooseBestSplit(dataSet, leafType=regLeaf, errType=regErr, ops=(1,2)):
    tolS = ops[0]; tolN = ops[1]
    if isSameVal(dataSet):
        return None, leafType(dataSet)
    m = len(dataSet)
    n = len(dataSet[0])
    S = errType(dataSet)
    bestS = float("inf"); bestIndex = 0; bestValue = 0
    for featIndex in range(n-1):
        for splitVal in getFeatSet(dataSet, featIndex):
            mat0, mat1 = binSplitDataSet(dataSet, featIndex, splitVal)
            if (len(mat0) < tolN) or (len(mat1) < tolN): continue
            newS = errType(mat0) + errType(mat1)
            if newS < bestS:
                bestIndex = featIndex
                bestValue = splitVal
                bestS = newS
    if (S - bestS) < tolS:
        return None, leafType(dataSet)
    mat0, mat1 = binSplitDataSet(dataSet, bestIndex, bestValue)
    if (len(mat0) < tolN) or (len(mat1) < tolN):
        return None, leafType(dataSet)
    return bestIndex, bestValue

def build(dataSet, leafType=regLeaf, errType=regErr, ops=(1,2)):
    feat, val = chooseBestSplit(dataSet, leafType, errType, ops)
    if feat == None: return val
    retTree = {}
    retTree['spInd'] = feat
    retTree['spVal'] = val
    lSet, rSet = binSplitDataSet(dataSet, feat, val)
    retTree['left'] = build(lSet, leafType, errType, ops)
    retTree['right'] = build(rSet, leafType, errType, ops)
    return retTree

def regTreeEval(model, inDat):
    return float(model)

def isTree(obj):
    return (type(obj).__name__=='dict')

def predict(tree, inData, modelEval=regTreeEval):
    if not isTree(tree): return modelEval(tree, inData)
    if inData[tree['spInd']] > tree['spVal']:
        if isTree(tree['left']):
            return predict(tree['left'], inData, modelEval)
        else:
            return modelEval(tree['left'], inData)
    else:
        if isTree(tree['right']):
            return predict(tree['right'], inData, modelEval)
        else:
            return modelEval(tree['right'], inData)

def makeFlavorTrain(k, train_X, train_y):
    res = copy.deepcopy(train_X)
    if k < 0 or k > 14: return
    for i in range(len(train_X)):
        res[i].append(train_y[i][k])
    return res

if __name__ == '__main__':
    raw = process_feat.TrainingSet('TrainData_2015.1.1_2015.2.19.txt',
                                   'input_5flavors_cpu_7days.txt')
    test_flavor = raw.get_flavorID()
    test_res = []
    print(test_flavor)
    train_X, train_y, test_feat = raw.getTrainFeat()
    for hoge in test_flavor:
        train_flavorID = makeFlavorTrain(hoge - 1, train_X, train_y)
        regTree = build(train_flavorID)
        test_res.append(round(predict(regTree, test_feat)))
    print(test_res)


