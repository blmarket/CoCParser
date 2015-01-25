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

def extract_kp(img):
    kps = feature.corner_peaks(feature.corner_harris(img), min_distance = 2)
    extractor = feature.BRIEF(patch_size = 5)
    extractor.extract(img, kps)
    return extractor.descriptors

def extract_kp_CENSURE(img, plot = None):
    d1 = feature.CENSURE(mode = 'STAR')
    d1.detect(img)
    if plot is not None:
        plot.imshow(img)
        plot.axis('off')
        plot.scatter(d1.keypoints[:, 1], d1.keypoints[:, 0])
    return d1.keypoints

def equal_group(it, jt):
    mx = feature.match_descriptors(it, jt)
    rate = float(len(mx)) * 2 / (len(it) + len(jt))
    return rate > 0.6

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
                dic[jt] += [ it ]
                break
        if not found:
            dic[it] = [ it ]
    return dic

if __name__ == "__main__":
    import engine
    import pandas as pd

    e = engine.get_engine()

    def getIds(label):
        df = pd.io.sql.read_sql_query(
                '''
                SELECT `id` FROM `src`
                WHERE `category` = '%s'
                ''' % (label), e
                )
        return list(df['id'])

    raw_keys = itertools.product(getIds('20150122'), xrange(2))
    keys = itertools.ifilter(lambda x: int(db_mysql.cache_attack(x)) >= 0, raw_keys)

    res = reduce_groups(keys, get_image, equal_group)

    plt.gray()
    fig, plots = plt.subplots(20, 5)
    for it in itertools.chain.from_iterable(plots):
        it.axis('off')

    idx = 0
    for it in res:
        if len(res[it]) == 1:
            continue
        for j, jt in enumerate(res[it]):
            if j >= 5:
                break
            print j, jt
            plots[idx][j].imshow(get_image(jt))
        idx += 1
        if idx >= 20:
            break

    plt.show()
    exit(0)
