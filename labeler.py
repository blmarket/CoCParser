import numpy as np
from skimage import io

def label(row):
    img = np.reshape(row, (52, 1024))
    io.imshow(img)

    yn = raw_input('YN? : ')
    if yn == 'Y' or yn == 'y':
        return 1
    else:
        return 0

## Current trials: df.loc[3, 'label'] = label(df.loc[3])
## type is problem.
