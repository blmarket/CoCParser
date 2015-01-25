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

if __name__ == "__main__":
    ts = range(4831, 4851)
    ts = ts[-5:]

    plt.gray()
    fig, plots = plt.subplots(nrows = len(ts), ncols = 2)

    for idx, it in enumerate(ts):
        x = load_image(it)
        t1, t2 = split_attacks(x)

        p1 = plots[idx][0]
        p2 = plots[idx][1]

        extract_kp(t1, plot = p1)
        extract_kp(t2, plot = p2)

    plt.show()
