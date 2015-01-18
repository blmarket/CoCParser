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
            last = it

def cell_ipad(slit):
    units = np.transpose(slit[59:120])

    for ix in range(114, 500, 49):
        io.imshow(np.transpose(units[ix:ix+46]))

if __name__ == "__main__":
    io.use_plugin('pil')
    for slit in split('src.png'):
        cell_ipad(slit)
        # io.imshow(slit)
        # io.imshow(skimage.filter.sobel(slit))
    sys.exit(0)
