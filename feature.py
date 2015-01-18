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

for it in range(4031, 4033):
    x = np.load(BytesIO(db_mysql.cache_mysql(str(it)))).reshape([52, 1024])

    detector = feature.CENSURE()
    detector.detect(x)

    plt.gray()
    plt.imshow(x)
    plt.scatter(detector.keypoints[:, 1], detector.keypoints[:, 0],
            2 ** detector.scales)
    plt.show()

