import sys
from skimage import data, io, filter, transform
import numpy as np

def preprocess(filename):
    image = io.imread(filename, as_grey = True)

    if image.shape[0] != 768:
        print(image.shape)
        print("WARN: Resizing image to old iPad Size. TODO> Move forward to retina images!")
        return transform.resize(image, (768, 1024))

    return image

def yield_slits(image):
    ff = filter.canny(image)
    pi = 0
    for i in range(len(ff)):
        cnt = np.count_nonzero(ff[i])
        if cnt > 800:
            diff = i - pi
            if diff > 50 and diff < 60:
                slit = image[i-52:i]
                yield slit
            pi = i

def parse(filename):
    image = preprocess(filename)
    return yield_slits(image)

def check_and_parse(filename):
    """
    Check whether enemy or not, and returns slit.
    """
    image = preprocess(filename)
    isEnemy = (image[55][600] < 0.7)
    for it in yield_slits(image):
        yield (isEnemy, it)

if __name__ == "__main__":
    io.use_plugin('pil')
    check_and_parse("9.png")
    for it in parse("9.png"):
        print(it)
