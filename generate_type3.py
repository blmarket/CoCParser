#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extract type 3 particles from images
"""
from models.engine import get_engine
from models.models import War, Src
from sqlalchemy.orm import Session
from slit_utils import cutfront

import numpy as np
import blobs
from StringIO import StringIO
from skimage import io

engine = get_engine()

session = Session(engine)

def add_splits(date, src_id):
    def save_img(arr):
        """saves image into src"""
        png = StringIO()
        io.imsave(png, arr)
        png_url = blobs.createBlob(date, png.getvalue())

        data_fp = StringIO()
        np.save(data_fp, arr)

        # TODO: Save image and data into src table and return its id

    save_img(cutfront((src_id, 0)))
    save_img(cutfront((src_id, 1)))
    print src_id

q = session.query(War).\
        filter(War.enemy == 1)

for it in q:
    add_splits(it.date, it.src_id)
