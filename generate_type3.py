#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extract type 3 particles from images
"""
from models.engine import get_engine
from models.models import War, Src
from sqlalchemy.orm import Session
from slit_utils import cutfront2

import numpy as np
import blobs
from io import BytesIO
from skimage import io

def add_splits(session, war, slit):
    date = war.date

    def save_img(arr):
        """saves image into src"""
        png = BytesIO()
        io.imsave(png, arr)
        png_url = blobs.createBlob(date, png.getvalue())

        row = Src(data_url = png_url,\
                type = 3)
        session.add(row)
        session.commit()
        return row.id

        # TODO: Save image and data into src table and return its id

    war.atk1_src, war.atk2_src = map(save_img, cutfront2(slit))
    session.commit()

if __name__ == "__main__":
    engine = get_engine()
    session = Session(engine)
    q = session.query(War).\
            filter(War.atk1_src == None).\
            filter(War.date >= '20150228')

    for it in q:
        print(it)
        add_splits(session, it)
