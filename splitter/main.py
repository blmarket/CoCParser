#!/usr/bin/env python

import sys
import skimage
from skimage import io, filter
import numpy as np

def split(filename):
    img = skimage.io.imread(filename, as_grey = True)

    c = skimage.filter.canny(img)

    last = None

    for it, row in enumerate(c):
        nw = np.count_nonzero(row)
        if nw > 500:
            if last is not None:
                space = it - last
                if space > 160:
                    slit = img[it-160:it]
                    yield slit
                print it - last, it, nw
            last = it


if __name__ == "__main__":
    for slit in split('src.png'):
        io.imshow(slit)
    sys.exit(0)
