#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TODO: fill this area
"""
from sys import exit, argv
from io import BytesIO
from skimage import io, feature, exposure
import skimage.filter as skf
import numpy as np
import json
from db_mysql import Session, Effectives
import db_mysql
import itertools
import logging

logging.basicConfig(level=logging.DEBUG)

def split_attacks(x):
    """
    Return attack slits from one attack image.
    positions are pre-calculated
    """
    return x[22:, 461:641], x[22:, 645:825] # iPad specific

orb = feature.ORB()

def extract_orb(img):
    print img
    orb.detect_and_extract(img)
    ret = orb.descriptors
    print ret
    return ret

def extract_kp(img):
    kps = feature.corner_peaks(feature.corner_harris(img), min_distance = 2)
    bb = feature.BRIEF(patch_size = 5) # iPad specific(or not)
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

def dumb_matcher(img1, img2):
    kps = lambda img: feature.corner_peaks(feature.corner_harris(img), min_distance = 2)
    kp1 = kps(img1)
    kp2 = kps(img2)
    to_set = lambda aoa: set(map(lambda x: (x[0], x[1]), aoa))
    s1 = to_set(kp1)
    s2 = to_set(kp2)
    return float(len(s1 & s2) * 2) / (len(s1) + len(s2))

def matcher(img_extractor):
    """calculate similarity
    img_extractor: takes image, returns feature point descriptors, as of writing this method, 'extractor_kp' is good example.
    """
    def calculate_rate(it, jt):
        mx = feature.match_descriptors(it, jt)
        return float(len(mx) * 2) / (len(it) + len(jt))

    def func(img1, img2):
        return calculate_rate(img_extractor(img1), img_extractor(img2))
    return func

"""Actual matcher being used"""
# default_matcher = matcher(extract_kp)
default_matcher = dumb_matcher

def get_image(key):
    def load_image(it):
        return np.load(BytesIO(db_mysql.cache_mysql(str(it)))).reshape([52, 1024])
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
                rate = compare(img, kmg)
                if rate < 0.70:
                    match = False
                    break
                print('match rate : %s %s %s' % (it, jt, rate))

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

def process(date):
    db_mysql.clear_tags(date)
    gs = generate_groups(date).values()
    s = Session()

    mosts = {}

    for i, it in enumerate(gs):
        fn = lambda (x, y): int(db_mysql.cache_tag(x, "atk_eff%s" % (y + 1)))
        atk_fn = lambda (x, y): int(db_mysql.cache_tag(x, "attack%s" % (y+1)))

        combined_fn = lambda v: -(atk_fn(v) * 10 + fn(v))

        arr = sorted(it, key = combined_fn)

        if atk_fn(arr[0]) > 0:
            nk = arr[0][0]
            if nk not in mosts: mosts[nk] = 0
            mosts[nk] += 1

        for j, jt in enumerate(arr):
            s.add(Effectives(date=date, src_id=jt[0], atk_id=jt[1], group_id=i, group_idx=j))
            s.commit()

    for it in mosts:
        db_mysql.add_tag(it, "most", mosts[it])

def cutfront(key):
    img = np.transpose(get_image(key))
    v = np.any(skf.canny(img), axis=1)
    pos = next((it[0] for it in enumerate(v) if it[1] == True), None)
    return img[pos:30] # iPad specific

# if __name__ == "__main__":
#     date = argv[-1]
#     process(date)
