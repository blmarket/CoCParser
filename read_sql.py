import sqlite3
import MySQLdb as mdb
import pickle
import pandas as pd
import numpy as np
from labeler import label

# con = sqlite3.connect('db.sqlite')
con = mdb.connect('localhost', 'root', '', 'cocparser')

df = pd.io.sql.read_frame('SELECT `src`.`id`, `DATA` FROM `src` LEFT JOIN `samples` ON src.id = src_id WHERE attack IS NULL ORDER BY RAND() LIMIT 10', con)

for i in xrange(len(df)):
    src_id = df.loc[i, 'id']
    lab = label(pickle.loads(df.loc[i, 'DATA']))

    con.query("""
    INSERT INTO `samples` (`src_id`, `attack`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE attack = %s;
    """ % (src_id, lab, lab))
    con.commit()
    print lab, df.loc[i, 'id']
