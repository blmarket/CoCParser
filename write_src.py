"""
writes src database.
database schema should be defined. see schema.sql
TODO: change serializer to protobuf?
"""
import sys

import glob
from itertools import chain
from parse import parse
import pandas as pd
import pickle
import sqlite3
import numpy as np
from flickr import fetch_images
from StringIO import StringIO
from skimage import io
import blobs
import json
from models import engine.get_engine

engine = get_engine()

def src_entries(L, title):
    for slit in L:
        png = StringIO()
        io.imsave(png, slit)
        png_url = blobs.createBlob(title, png.getvalue())
        print png_url, type(slit)

        data_fp = StringIO()
        np.save(data_fp, np.array(list(slit.flatten())))

        type_id = 1
        if title[0] == 'E':
            type_id = 2

        yield [ data_fp.getvalue(), png.getvalue(), title, png_url, type_id ]

def write_src(L, title):
    for row in src_entries(L, title):
        df = pd.DataFrame( [ it ], columns = [ 'DATA', 'PNG', 'category', 'data_url', 'type' ])
        pd.io.sql.write_frame(df, 'src', engine, flavor = 'mysql', if_exists = 'append')

if __name__ == "__main__":
    title = sys.argv[-1]
    L = chain.from_iterable(parse(filename) for filename in fetch_images(title))

    write_src(L, title)
