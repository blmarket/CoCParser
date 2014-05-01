"""
writes src database.
"""
import glob
from itertools import chain
from parse import parse
import pandas as pd
import pickle
import MySQLdb as mdb
import sqlite3

L = chain.from_iterable(parse(filename) for filename in glob.glob('*.png'))
LL = (pickle.dumps(list(it)) for it in L)

df = pd.DataFrame(list(LL), columns = ['DATA'])

con = mdb.connect('localhost', 'root', '', 'cocparser')
# con = sqlite3.connect('db.sqlite')

"""
database schema should be defined. otherwise possible loss of data due to invalid data type.

CREATE TABLE src (
  `id` int NOT NULL auto_increment,
  `data` mediumblob,
  PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8; 
"""

for i in range(len(df)):
    pd.io.sql.write_frame(df[i:i+1], 'src', con, flavor = 'mysql', if_exists = 'append')
    con.commit()

# print df
con.commit()
