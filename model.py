import pandas as pd
from skimage import io
import sklearn
import numpy as np

df = pd.read_csv('train.csv', index_col = 0)

cnt = 0
for it in df.iterrows():
    cnt += 1
    if cnt > 3:
        break
    index = it[0]
    arr = it[1].values[1:]
    img = np.reshape(arr, (52, 1024))
    io.imshow(img)
    label = raw_input("Enter Y/N for given image : ")
    if label == 'Y' or label == 'y':
        dic[index] = 'Y'
    else:
        dic[index] = 'N'

