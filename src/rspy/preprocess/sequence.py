import numpy as np
from numpy.lib.stride_tricks import as_strided

def getRolling(data, windowSize):
    sliceSize = len(data) - windowSize + 1
    if sliceSize <= 0:
        raise ValueError("Rolling not possible, windowSize is larger then data length.")

    shape = (sliceSize, windowSize) + data.shape[1:]
    strides = (data.strides[0],) + data.strides

    return as_strided(data, shape=shape, strides=strides)

