from skimage import data, io, filter
import numpy as np

FILENAME = '0.png'

image = io.imread(FILENAME, as_grey = True)

ff = filter.canny(image)
# io.imshow(ff)

pi = 0
for i in xrange(len(ff)):
    cnt = np.count_nonzero(ff[i])
    if cnt > 800:
        diff = i - pi
        if diff > 50 and diff < 60:
            slit = image[i-52:i]
            data = slit.flatten()
            io.imshow(slit)
        print i, cnt, i-pi
        pi = i
    # , ff[i].choose(set([True]))

