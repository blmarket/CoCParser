"""
writes src database.
database schema should be defined. see schema.sql
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

title = '20140505'

# L = chain.from_iterable(parse(filename) for filename in glob.glob('*.png'))
L = chain.from_iterable(parse(filename) for filename in fetch_images(title))
# LL = (pickle.dumps(list(it.flatten())) for it in L)

con = mdb.connect('localhost', 'root', '', 'cocparser')
for slit in L:
    png = StringIO()
    io.imsave(png, slit)

    row = pickle.dumps(list(slit.flatten()))
    df = pd.DataFrame([ [ row, png.getvalue(), title ] ], columns = ['DATA', 'PNG', 'category'])

    pd.io.sql.write_frame(df, 'src', con, flavor = 'mysql', if_exists = 'append')
    con.commit()

# con = sqlite3.connect('db.sqlite')
