"""
writes src database.
database schema should be defined. see schema.sql
TODO: change serializer to protobuf?
"""
import glob
from itertools import chain
from parse import parse
import pandas as pd
import pickle
from sqlalchemy import create_engine
import sqlite3
import numpy as np
from flickr import fetch_images
from StringIO import StringIO
from skimage import io
import blobs
import json

config = None
with open('config.json') as conf:
    config = json.load(conf)

if not config:
    exit(-1)

conn_str = "mysql://%s:%s@%s/%s" % (config[u'user'], config[u'password'], config['host'], config['database'])
engine = create_engine(conn_str, encoding = 'utf8')

def write_src(L, title):
    for slit in L:
        png = StringIO()
        io.imsave(png, slit)
        png_url = blobs.createBlob(title, png.getvalue())
        print png_url, type(slit)

        data_fp = StringIO()
        np.save(data_fp, np.array(list(slit.flatten())))

        df = pd.DataFrame([ [ data_fp.getvalue(), png.getvalue(), title, png_url, 1 ] ], columns = ['DATA', 'PNG', 'category', 'data_url', 'type'])

        pd.io.sql.write_frame(df, 'src', engine, flavor = 'mysql', if_exists = 'append')

if __name__ == "__main__":
    title = '20140808'
    L = chain.from_iterable(parse(filename) for filename in fetch_images(title))

    write_src(L, title)
