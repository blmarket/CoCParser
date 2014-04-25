import pandas as pd
from skimage import io
import sklearn
import numpy as np

df = pd.read_csv('xs.csv', index_col = 0)

df['label'] = [None] * len(df)

df.to_csv('train.csv')
