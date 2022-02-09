import math
import numpy as np
import matplotlib.pylab as plt

def getImageSliced(imageData, rowSliceCnt, colSliceCnt, stride=1):
    imgWidth  = int(imageData.shape[0] / rowSliceCnt)
    imgHeight = int(imageData.shape[1] / colSliceCnt)
    
    images = []
    rowStart = 0
    colStart = 0
    
    while rowStart + imgWidth <= imageData.shape[1]:
        while colStart + imgHeight <= imageData.shape[0]:
            image = imageData[rowStart:rowStart + imgWidth, colStart:colStart + imgHeight, :]
            images.append(image)
            colStart += stride
        rowStart += stride
        colStart = 0

    return np.array(images)

def showImagesGrid(imageDatas, colCnt=None, rowCnt=None, gap=0.03, sigsize=5, cmap=None):
    plt.figure(figsize=(sigsize, sigsize))
    imgSize = len(imageDatas)
    if cmap is None:
        cmap = plt.get_cmap('gray')
    
    if rowCnt is None:
        if colCnt is None:
            colCnt = math.ceil(math.sqrt(imgSize))
        rowCnt = colCnt
        
    for idx in range(imgSize):
        plt.subplot(colCnt, rowCnt, idx+1)
        plt.imshow(imageDatas[idx], cmap=cmap)
        plt.axis("off")
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, 
                        wspace=gap, hspace=gap)
    plt.show()
