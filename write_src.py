"""
writes src database.
"""
import glob
from itertools import chain
from parse import parse
import pandas as pd
import json
import sqlite3

L = chain.from_iterable(parse(filename) for filename in glob.glob('*.png'))
LL = (json.dumps(list(it)) for it in L)

df = pd.DataFrame(list(LL), columns = ['DATA'])

con = sqlite3.connect('db.sqlite')
pd.io.sql.write_frame(df, 'src', con, if_exists = 'replace')
# print df
