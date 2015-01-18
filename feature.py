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
    return x[:, 460:645], x[:, 645:830]

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

if __name__ == "__main__":
    for it in range(4031, 4051):
        x = load_image(it)
        t1, t2 = split_attacks(x)

        # io.imshow(t1, 'pil')
        # io.imshow(t2, 'pil')

        d1 = feature.CENSURE()
        d2 = feature.CENSURE()

        d1.detect(t1)
        d2.detect(t2)

        print feature.match_descriptors(d1.keypoints, d2.keypoints)
