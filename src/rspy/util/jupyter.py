import os, math, re, warnings, logging
import tensorflow as tf
import ipywidgets as ipw
from matplotlib import font_manager
import pandas as pd

def showMulti(*args, colSize=None, width="100%", margin="3px"):
    """Display multiple output data lines and columns as desired.
    Args:
      args: multiple datas.
      colSize: column size.
      width: css style width parameter. default is 100%. you can use "px" unint.
      margin: css style margin parameter. default is 3px.
    Returns:
      None
    Example:
      >>> showMulti("a", "b", "c", colSize=2)
      a      b
      c
    """

    # calculate column and row counts.
    lenArgs = len(args)
    if (colSize is not None) and (colSize > 0) and (lenArgs - colSize > 0):
        lenRow = math.ceil(lenArgs/colSize)
        lenCol = colSize
    else:
        lenRow = 1
        lenCol = lenArgs

    # create Output() of ipywidgets and to display the args to it.
    layout = ipw.Layout(width=width, grid_gap=margin)
    grid = ipw.GridspecLayout(lenRow, lenCol, layout=layout)
    outs = [ipw.Output() for _ in range(len(args))]
    for idx, out in enumerate(outs):
        with out:
            display(args[idx])

    # allocate Output() to grid
    idxOuts = 0
    for row in range(lenRow):
        for col in range(lenCol):
            grid[row, col] = outs[idxOuts] if idxOuts < lenArgs else ipw.Output()
            idxOuts += 1
    display(grid)

def getSystemFonts(hintRegex=""):
    regex = re.compile(hintRegex, re.IGNORECASE)
    return [{f.name: f.fname} for f in font_manager.fontManager.ttflist if regex.search(f.fname)]

def setSystemWarning(off=True):
    warnings.filterwarnings(action="ignore" if off else "default")
    logging.getLogger("tensorflow").setLevel(logging.FATAL if off else logging.INFO)

def printDataframeAllRow(dataframe, sizeSample=None):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None):
        display(dataframe if sizeSample is None else dataframe.sample(sizeSample))

def fixMemoryProblem():
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            # Currently, memory growth needs to be the same across GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            print(e)
