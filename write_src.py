"""
writes src database.
database schema should be defined. see schema.sql
TODO: change serializer to protobuf?
"""
import sys

import glob
from itertools import chain
from parse import parse, check_and_parse
import pandas as pd
import pickle
import sqlite3
import numpy as np
from flickr import fetch_images
from io import BytesIO
from skimage import io
import blobs
import json
from models.engine import get_engine
from models.models import Src, War
from sqlalchemy.orm import Session
from generate_type3 import add_splits

engine = get_engine()

def src_entries(L, title):
    for isEnemy, slit in L:
        png = BytesIO()
        io.imsave(png, slit)
        png_url = blobs.createBlob(title, png.getvalue())
        print(png_url, type(slit))

        data_fp = BytesIO()
        np.save(data_fp, np.array(list(slit.flatten())))

        type_id = 1
        if isEnemy:
            type_id = 2

        yield [ slit, png.getvalue(), title, png_url, type_id ]

def write_src(L, title):
    session = Session(engine)
    for row in src_entries(L, title):
        src = Src(category = row[2], data_url = row[3], type = row[4])
        session.add(src)
        session.commit()

        war = War(date = src.category, enemy = src.type - 1, src_id = src.id)
        session.add(war)
        session.commit()

        add_splits(session, war, row[0])

if __name__ == "__main__":
    title = sys.argv[-1]
    L = chain.from_iterable(check_and_parse(filename) for filename in fetch_images(title))

    write_src(L, title)
