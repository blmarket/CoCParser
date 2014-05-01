import sqlite3
import MySQLdb as mdb
import pickle
import pandas as pd
import numpy as np
from labeler import label

# con = sqlite3.connect('db.sqlite')
con = mdb.connect('localhost', 'root', '', 'cocparser')

df = pd.io.sql.read_frame('SELECT `id`, `DATA` FROM `src` WHERE id = 41', con)

for i in xrange(len(df)):
    src_id = df.loc[i, 'id']
    lab = label(pickle.loads(df.loc[i, 'DATA']))
