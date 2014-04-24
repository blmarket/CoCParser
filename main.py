from skimage import data, io, filter
import numpy as np

image = io.imread('maruta.png', as_grey = True)

ff = filter.canny(image)
pi = 0
for i in xrange(len(ff)):
    cnt = np.count_nonzero(ff[i])
    if cnt > 800 and cnt < 900:
        diff = i - pi
        if diff > 50 and diff < 60:
            io.imshow(image[pi:i])
        print i, cnt, i-pi
        pi = i
    # , ff[i].choose(set([True]))

# io.imshow(ff)
