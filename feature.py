#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TODO: fill this area
"""
from sys import exit
from io import BytesIO
from skimage import io, feature
import numpy as np
import json
import db_mysql
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

def generate_groups(date):
    raw_keys = itertools.product(db_mysql.cache_ids(date), xrange(2))
    keys = itertools.ifilter(lambda x: int(db_mysql.cache_attack(x)) >= 0, raw_keys)

    return reduce_groups(keys, get_image, default_matcher)

gs = json.loads("""[[[5184, 0], [5197, 0]], [[5159, 0]], [[5164, 0], [5192, 1]], [[5158, 1], [5178, 0]], [[5155, 1], [5157, 1], [5159, 1], [5160, 1], [5161, 1], [5163, 1], [5167, 1], [5171, 1], [5175, 1], [5178, 1], [5180, 1], [5181, 1], [5182, 1], [5188, 1], [5196, 0]], [[5190, 0]], [[5168, 1]], [[5154, 0]], [[5187, 1]], [[5180, 0], [5181, 0]], [[5174, 1], [5191, 0], [5193, 1]], [[5185, 0]], [[5165, 0], [5175, 0]], [[5184, 1]], [[5170, 0]], [[5164, 1]], [[5155, 0]], [[5183, 0]], [[5190, 1], [5194, 1]], [[5160, 0], [5169, 1]], [[5154, 1]], [[5186, 0]], [[5177, 1]], [[5171, 0]], [[5156, 0], [5157, 0], [5162, 0]], [[5191, 1]], [[5161, 0]], [[5182, 0]], [[5187, 0], [5195, 0]], [[5173, 1], [5176, 0], [5177, 0]], [[5167, 0], [5170, 1]], [[5186, 1]], [[5172, 0]], [[5166, 1]], [[5198, 0]], [[5189, 1], [5198, 1]], [[5156, 1], [5163, 0], [5173, 0]], [[5188, 0]], [[5193, 0]], [[5179, 1], [5192, 0], [5196, 1], [5197, 1]], [[5172, 1], [5176, 1]], [[5158, 0], [5165, 1], [5166, 0], [5169, 0]], [[5168, 0], [5174, 0], [5179, 0]], [[5189, 0]], [[5194, 0]], [[5183, 1], [5185, 1]]]""")

gs = generate_groups('20150130').values()

for it in gs:
    fn = lambda (x, y): int(db_mysql.cache_tag(x, "atk_eff%s" % (y + 1)))
    atk_fn = lambda (x, y): int(db_mysql.cache_tag(x, "attack%s" % (y+1)))

    fxx = filter(lambda x: fn(x) > 0, it)
    if len(fxx) == 0:
        continue

    mark_fn = lambda (x, y): db_mysql.mark_most(x, y + 1)

    mark_fn(max(fxx, key = atk_fn))
