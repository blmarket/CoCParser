import numpy as np
from skimage import io

def label(row):
    img = np.reshape(row, (52, 1024))
    io.imshow(img)

    return raw_input('label? : ')

## Current trials: df.loc[3, 'label'] = label(df.loc[3])
## type is problem.
