import glob
from skimage import data, io, filter
import numpy as np
import pandas as pd

files = glob.glob('*.png')

agg = pd.DataFrame()

for f in files:
    print f
    image = io.imread(f, as_grey = True)
    ff = filter.canny(image)

    pi = 0
    for i in xrange(len(ff)):
        cnt = np.count_nonzero(ff[i])
        if cnt > 800:
            diff = i - pi
            if diff > 50 and diff < 60:
                slit = image[i-52:i]
                data = pd.Series(slit.flatten())
                if agg.empty == True:
                    agg = pd.DataFrame(data).transpose()
                else:
                    agg = agg.append(data, ignore_index = True)
                # io.imshow(slit)
            print i, cnt, i-pi
            pi = i

agg.to_csv('xs.csv')
