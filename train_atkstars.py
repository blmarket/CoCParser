"""
Train and create prediction.
"""
import pickle
import pandas as pd
import MySQLdb as mdb
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier as RF
import numpy as np
import json

LABEL_NAME = 'atkstars'
PREDICT_NAME = 'predict_' + LABEL_NAME

config = json.load(open('config.json'))

con = mdb.connect(config[u'host'], config[u'user'], config[u'password'], config[u'database'])

df = pd.io.sql.read_frame('''
SELECT `src`.`id`, `DATA`, `samples`.`%s` 
FROM `src` LEFT JOIN `samples` ON `src`.`id` = `samples`.`src_id`
WHERE `%s` IS NOT NULL ORDER BY RAND()
LIMIT 100
''' % (LABEL_NAME, LABEL_NAME), con)

X = pd.DataFrame(list(df['DATA'].map(lambda x: np.array(pickle.loads(x), dtype=np.float64))))
y = df[LABEL_NAME]

print X
print y

rf = RF()
rf.fit(X, y)

test_set = pd.io.sql.read_frame('''
SELECT `src`.`id`, `DATA` 
FROM `src` LEFT JOIN `samples` ON `src`.`id` = `samples`.`src_id`
WHERE (samples.attack OR samples.predict_attack) AND `samples`.`%s` IS NULL
LIMIT 1000
''' % (LABEL_NAME), con)

for i in xrange(len(test_set)):
    src_id = test_set.loc[i, 'id']

    Xrow = list(pickle.loads(test_set.loc[i, 'DATA']))
    lab = rf.predict(Xrow)[0]

    print src_id, lab

    con.query("""
    INSERT INTO `samples` (`src_id`, `%s`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `%s` = %s;
    """ % (PREDICT_NAME, src_id, lab, PREDICT_NAME, lab))
    con.commit()
