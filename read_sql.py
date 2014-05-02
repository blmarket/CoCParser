import sqlite3
import MySQLdb as mdb
import pickle
import pandas as pd
import numpy as np
from labeler import label

# con = sqlite3.connect('db.sqlite')
con = mdb.connect('localhost', 'root', '', 'cocparser')

PRECONDITION = '`predict_attack` = 1'
PRECONDITION = '1'
LABEL_NAME = 'attack'

df = pd.io.sql.read_frame('''
SELECT `src`.`id`, `DATA` FROM `src` LEFT JOIN `samples` ON src.id = src_id 
WHERE %s  
AND `%s` IS NULL
ORDER BY RAND() 
LIMIT 20
''' % (PRECONDITION, LABEL_NAME), con)

for i in xrange(len(df)):
    src_id = df.loc[i, 'id']
    lab = label(pickle.loads(df.loc[i, 'DATA']))

    con.query("""
    INSERT INTO `samples` (`src_id`, `%s`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `%s` = %s;
    """ % (LABEL_NAME, src_id, lab, LABEL_NAME, lab))
    con.commit()
    print lab, df.loc[i, 'id']
