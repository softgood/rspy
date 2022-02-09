import matplotlib.pyplot as plt

def plotHistory(history, figsize=(12, 4)):
    plt.figure(figsize=figsize)
    plt.style.use("ggplot")
    histKeys = history.history.keys()
    plotCnt = 0
    if 'loss' in histKeys: plotCnt += 1
    if 'val_loss' in histKeys: plotCnt += 1
    
    subPosition = 1
    if 'loss' in histKeys:
        plt.subplot(1, plotCnt, subPosition)
        plt.plot(history.history['loss'], 'r-', label='loss')
        if 'accuracy' in histKeys: plt.plot(history.history['accuracy'], 'g-', label='accuracy')
        plt.title("Training Loss and Accuracy")
        plt.xlabel('Epoch')
        plt.legend()
        subPosition += 1

    if 'val_loss' in histKeys:
        plt.subplot(1, plotCnt, subPosition)
        plt.plot(history.history['val_loss'], 'r-', label='val_loss')
        if 'val_accuracy' in histKeys: plt.plot(history.history['val_accuracy'], 'g-', label='val_accuracy')
        plt.title("Validation Loss and Accuracy")
        plt.xlabel('Epoch')
        plt.legend()

    plt.show()
