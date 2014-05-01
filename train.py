import pickle
import pandas as pd
import MySQLdb as mdb
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier as RF
import numpy as np

con = mdb.connect('localhost', 'root', '', 'cocparser')

df = pd.io.sql.read_frame('SELECT `src`.`id`, `DATA`, `attack` FROM `src` LEFT JOIN `samples` ON src.id = src_id WHERE attack IS NOT NULL LIMIT 1000', con)

X = pd.DataFrame(list(df['DATA'].map(lambda x: np.array(pickle.loads(x), dtype=np.float64))))
y = df['attack']

print df['DATA']
print df['attack']

rf = RF()
rf.fit(X, y)

test_set = pd.io.sql.read_frame('SELECT `id`, `DATA` FROM `src` LIMIT 1000', con)

for i in xrange(len(test_set)):
    src_id = test_set.loc[i, 'id']

    Xrow = list(pickle.loads(test_set.loc[i, 'DATA']))
    lab = rf.predict(Xrow)[0]

    con.query("""
    INSERT INTO `samples` (`src_id`, `predict_attack`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `predict_attack` = %s;
    """ % (src_id, lab, lab))
    con.commit()
