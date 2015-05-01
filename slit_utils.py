#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from io import BytesIO
from models import db_mysql
import skimage.feature as skf

def split_attacks(x):
    """
    Return attack slits from one attack image.
    positions are pre-calculated
    """
    return x[22:, 461:641], x[22:, 645:825] # iPad specific

def get_image(key):
    def load_image(it):
        return np.load(BytesIO(db_mysql.cache_mysql(str(it)))).reshape([52, 1024])
    idx, lr = key
    return split_attacks(load_image(idx))[lr]

def __cutfront(img):
    img = np.transpose(img)
    v = np.any(skf.canny(img), axis=1)
    pos = next((it[0] for it in enumerate(v) if it[1] == True), None)
    return np.transpose(img[pos:][:30]) # iPad specific

def cutfront2(img):
    return map(__cutfront, split_attacks(img))

def cutfront(key):
    return __cutfront(get_image(key))
