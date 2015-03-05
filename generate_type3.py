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

def add_splits(war):
    date = war.date

    def save_img(arr):
        """saves image into src"""
        png = StringIO()
        io.imsave(png, arr)
        png_url = blobs.createBlob(date, png.getvalue())

        data_fp = StringIO()
        np.save(data_fp, arr)

        row = Src(DATA = data_fp.getvalue(),\
                data_url = png_url,\
                type = 3)
        session.add(row)
        session.commit()
        return row.id

        # TODO: Save image and data into src table and return its id

    war.atk1_src = save_img(cutfront((war.src_id, 0)))
    war.atk2_src = save_img(cutfront((war.src_id, 1)))
    session.commit()

q = session.query(War).\
        filter(War.atk1_src == None).\
        filter(War.date >= '20150228')

for it in q:
    print it
    add_splits(it)
