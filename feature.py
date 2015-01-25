#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TODO: fill this area
"""
from sys import exit
from io import BytesIO
from skimage import io
from skimage import feature
import numpy as np
import json
import db_mysql
from matplotlib import pyplot as plt
import itertools

def split_attacks(x):
    """
    Return attack slits from one attack image.
    positions are pre-calculated
    """
    return x[21:, 460:645], x[21:, 645:830]

def load_image(it):
    return np.load(BytesIO(db_mysql.cache_mysql(str(it)))).reshape([52, 1024])

def example_check_first_occurrence():
    """
    For split two attack fields from one shot,
    I checked first occurrence of feature point.
    """
    for it in range(4031, 4033):
        x = load_image(it)

        detector = feature.CENSURE()
        detector.detect(x)

        plt.gray()
        plt.imshow(x)
        print sorted(filter(lambda x: x>460, detector.keypoints[:, 1]))
        plt.scatter(detector.keypoints[:, 1], detector.keypoints[:, 0],
                2 ** detector.scales)
        # plt.show()
        # TODO: use matcher.

def extract_kp(img, plot = None):
    d1 = feature.CENSURE()
    d1.detect(img)
    if plot is not None:
        plot.imshow(img)
        plot.axis('off')
        plot.scatter(d1.keypoints[:, 1], d1.keypoints[:, 0])
    return d1.keypoints

def equal_group(it, jt):
    mx = feature.match_descriptors(it, jt)
    rate = float(len(mx)) * 2 / (len(it) + len(jt))
    return rate > 0.7

def get_image(key):
    idx, lr = key
    return split_attacks(load_image(idx))[lr]

def reduce_groups(keys, image_src, compare):
    """Clustering similar images

    Parameters
    ----------

    kv: [ key ] iterable
    image_src: method which accepts key and returns image for that key
    compare: method which accepts (image, image) and returns Boolean

    Returns
    -------

    { unique_id: [ keys ] } dict
    """
    dic = { }
    for it in keys:
        img = image_src(it)
        found = False
        for jt in dic:
            jmg = get_image(jt)
            if compare(img, jmg):
                found = True
                dic[jt] += it
                break
        if not found:
            dic[it] = [ it ]
    return dic

keys = itertools.chain.from_iterable([[ (x,0), (x,1) ] for x in range(4831, 4881)])

res = reduce_groups(keys, get_image, equal_group)
for it in res:
    print json.dumps(it), len(res[it])
exit(0)

if __name__ == "__main__":
    ts = range(4831, 4881)
    # ts = ts[-5:]

    plt.gray()

    nsample = 30
    fig, plots = plt.subplots(nrows = nsample, ncols = 5)
    for it in itertools.chain.from_iterable(plots):
        it.axis('off')

    def images():
        for it in ts:
            t1, t2 = split_attacks(load_image(it))
            yield t1
            yield t2

    def kps():
        for it, jt in itertools.izip(images(), itertools.chain.from_iterable(plots)):
            yield it, extract_kp(it)

    ks = list(kps())
    res = np.empty((len(ks), len(ks)), dtype=float)
    for i, (img, it) in enumerate(ks[:nsample]):
        idx = 0
        for j, (jmg, jt) in enumerate(ks):
            mx = feature.match_descriptors(it, jt)
            rate = float(len(mx)) * 2 / (len(it) + len(jt))
            res[i][j] = rate
            if rate > 0.7 and idx < 5:
                plots[i][idx].imshow(jmg)
                idx += 1
            None

    np.set_printoptions(linewidth = 130)
    print res
    plt.show()
