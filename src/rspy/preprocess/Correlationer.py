import numpy as np
import pandas as pd
import copy

class Correlationer:
    def __init__(self, method="pearson", critical=0.7, movingAverageWindow=2, movingWeightMax=2):
        self._method = method
        self._critical = critical
        self._movingAverageWindow = movingAverageWindow
        self._movingWeightMax = movingWeightMax
        self._corrListPositive = None
        self._corrListNegative = None
    
    def fit(self, dataframe, targetColumns, combine=False, removeCombineColumn=False, removeSubCombineColumn=True, removeOriginColumn=False):
        self._targetColumns = targetColumns
        self._removeCombineColumn = removeCombineColumn
        self._removeSubCombineColumn = removeSubCombineColumn
        self._removeOriginColumn = removeOriginColumn
        corr = dataframe[targetColumns].corr(method=self._method).to_numpy()

        corrColumB, corrRowB = np.where((corr > self._critical) & (corr < 1))
        corrColumS, corrRowS = np.where((corr < -self._critical) & (corr > -1))
        
        self._corrListPositive = []
        self._corrListNegative = []
        self._combinedColumns = set()
        for position in zip(corrColumB, corrRowB):
            if position[0] < position[1]:
                name1 = targetColumns[position[0]]
                name2 = targetColumns[position[1]]
                self._corrListPositive.append([name1, name2])
                self._combinedColumns.add(name1)
                self._combinedColumns.add(name2)
        for position in zip(corrColumS, corrRowS):
            if position[0] < position[1]:
                name1 = targetColumns[position[0]]
                name2 = targetColumns[position[1]]
                self._corrListNegative.append([name1, name2])
                self._combinedColumns.add(name1)
                self._combinedColumns.add(name2)
        self._combinedColumns = list(self._combinedColumns)
        
        if combine:
            self._corrListPositive = self._combine(self._corrListPositive)
            self._corrListNegative = self._combine(self._corrListNegative)
        
        return self._corrListPositive, self._corrListNegative
    
    def generate(self, dataframe):
        self._generatedColumns = []
        for item in self._corrListPositive:
            vals = []
            for name in item:
                vals.append(dataframe[name].astype(float).values)
            colName = "_".join(item)
            dataframe[colName] = self._all_diff(vals)
            self._generatedColumns.append(colName)
    
        for item in self._corrListNegative:
            vals = []
            for name in item:
                vals.append(dataframe[name].astype(float).values)
            colName = "_".join(item)
            dataframe[colName] = self._all_diff(vals)
            self._generatedColumns.append(colName)

        if self._removeOriginColumn:
            dataframe.drop(self._targetColumns, axis=1, inplace=True)

        if self._removeCombineColumn:
            dataframe.drop(self._combinedColumns, axis=1, inplace=True)
        
    def fit_generate(self, dataframe, targetColumns, combine=False, removeCombineColumn=False, removeSubCombineColumn=True, removeOriginColumn=False):
        self.fit(dataframe, targetColumns, combine, removeCombineColumn, removeSubCombineColumn, removeOriginColumn)
        self.generate(dataframe)
    
    def getColumnsTarget(self):
        return self._targetColumns

    def getColumnsGenerated(self):
        return self._generatedColumns

    def getColumns(self):
        result = set(self._targetColumns.tolist() + self._generatedColumns)

        if self._removeOriginColumn:
            result -= set(self._targetColumns)
        if self._removeCombineColumn:
            result -= set(self._combinedColumns)

        return list(result)
    
    def _combine(self, corrList):
        res = []
        if len(corrList) == 0:
            return res

        for item in corrList:
            isNew = True
            item = copy.copy(item)
            for x in res:
                if item[0] == x[1]:
                    x_copy = copy.deepcopy(x)
                    res.append(x_copy)

                    x[0].append(item[1])
                    x[1] = item[1]
                    isNew = False
                    break
            if isNew:
                res.append([item, item[1]])
            elif self._removeSubCombineColumn == False:
                res.append([item, item[1]])
        return sorted(np.array(res)[:,0].tolist())
    
    def _all_diff(self, vals):
        my = vals[0]
        other = vals[1:]

        diff = 0
        if len(other) > 1:
            diff += self._all_diff(other)
        
        myMA = self._moving_average(my, self._movingAverageWindow)
        for item in other:
            diff += self._moving_average(item, self._movingAverageWindow) - myMA

        return diff
    
    def transMovingDiffAverage(self, dataframe, targetColumns, windows=3):
        for colum in targetColumns:
            dataframe[colum] = self._moving_average(dataframe[colum].values, windows)
    
    def _moving_average(self, vals, windows=5):
        # 가중이동평균을 위한 가중값 생성
        weights = np.ones(windows)
        weightMax = windows if windows < self._movingWeightMax else self._movingWeightMax
        for idx in range(weightMax):
            weights[idx] = weightMax-idx

        # 가중 이동평균 계산
        stepVals = []
        stepVals.append(vals)
        temp = vals
        for idx in range(windows):
            temp = np.insert(temp[:-1], 0, temp[0])
            stepVals.append(temp)
        
        result = np.zeros([len(vals)])
        for idx, weight in zip(range(windows), weights):
            result += (stepVals[idx]*weight) - (stepVals[idx+1]*(1 if weight == 1 else weight-1))
        
        return result/weights.sum()

    def getCorrelationList(self):
        return self._corrListPositive, self._corrListNegative
    
    def __repr__(self):
        return f'{self._method}[critical: {self._critical}, positive: {self._corrListPositive}, negative: {self._corrListNegative}]'