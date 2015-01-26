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


orb = feature.ORB()

def extract_orb(img):
    print img
    orb.detect_and_extract(img)
    ret = orb.descriptors
    print ret
    return ret

def extract_kp(img):
    kps = feature.corner_peaks(feature.corner_harris(img), min_distance = 2)
    bb = feature.BRIEF(patch_size = 18)
    bb.extract(img, kps)
    return bb.descriptors

def extract_kp_CENSURE(img, plot = None):
    d1 = feature.CENSURE(mode = 'STAR')
    d1.detect(img)
    if plot is not None:
        plot.imshow(img)
        plot.axis('off')
        plot.scatter(d1.keypoints[:, 1], d1.keypoints[:, 0])
    return d1.keypoints

def matcher(method):
    threshold_rate = 0.85

    def equal_group(it, jt):
        mx = feature.match_descriptors(it, jt)
        rate = float(len(mx)) * 2 / (len(it) + len(jt))
        if rate > threshold_rate:
            print rate
        return rate > threshold_rate

    def func(a, b):
        return equal_group(method(a), method(b))
    return func

"""Actual matcher being used"""
default_matcher = matcher(extract_kp)

def get_image(key):
    idx, lr = key
    return split_attacks(load_image(idx))[lr]

def reduce_groups(keys, image_src, compare):
    """Clustering similar images

    TODO: Should use union find algorithm for better efficiency.

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
            match = True
            for kt in dic[jt]:
                kmg = image_src(kt)
                if not compare(img, kmg):
                    match = False
                    break

            if not match:
                continue

            found = True
            dic[jt] += [ it ]
            break
        if not found:
            dic[it] = [ it ]
    return dic

if __name__ == "__main__":
    raw_keys = itertools.product(db_mysql.cache_ids('20150126'), xrange(2))
    keys = itertools.ifilter(lambda x: int(db_mysql.cache_attack(x)) >= 0, raw_keys)

    res = reduce_groups(keys, get_image, default_matcher)

    max_matches = 45
    fig, plots = plt.subplots(max_matches, 5)
    plt.gray()
    for it in itertools.chain.from_iterable(plots):
        it.axis('off')

    for it in res:
        tmp = filter(lambda (src_id, idx): int(db_mysql.cache_tag(src_id, "atk_eff%s" % (idx+1))) > 0, res[it])
        if len(tmp) == 0:
            plots[0][0].imshow(get_image(res[it][0]))

    idx = 1
    for it in res:
        for j, jt in enumerate(res[it]):
            if j >= 5:
                break
            print j, jt
            plots[idx][j].imshow(get_image(jt))
            plots[idx][j].set_title(jt)
        idx += 1
        if idx >= max_matches:
            break

    plt.show()
