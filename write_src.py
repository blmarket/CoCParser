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
import MySQLdb as mdb
import sqlite3
from flickr import fetch_images
from StringIO import StringIO
from skimage import io
import blobs
import json

title = '20140530'

L = chain.from_iterable(parse(filename) for filename in fetch_images(title))

config = json.load(open('config.json'))

con = mdb.connect(config[u'host'], config[u'user'], config[u'password'], config[u'database'])

for slit in L:
    png = StringIO()
    io.imsave(png, slit)
    png_url = blobs.createBlob(title, png.getvalue())
    print png_url

    row = pickle.dumps(list(slit.flatten()))
    df = pd.DataFrame([ [ row, png.getvalue(), title, png_url, 1 ] ], columns = ['DATA', 'PNG', 'category', 'data_url', 'type'])

    pd.io.sql.write_frame(df, 'src', con, flavor = 'mysql', if_exists = 'append')
    con.commit()
