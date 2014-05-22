"""
Train and create prediction.
FIXME: duplicate code with train.py
"""
import pickle
import pandas as pd
import MySQLdb as mdb
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier as RF
from skimage import io
import numpy as np
import json

config = json.load(open('config.json'))

con = mdb.connect(config[u'host'], config[u'user'], config[u'password'], config[u'database'])

def getOne(pid):
    cur = con.cursor()
    cur.execute("SELECT id, type, field_name FROM `predictions` WHERE `id` = '%s' LIMIT 1" % (pid))
    row = cur.fetchone()
    cur.close()
    return row

def getTrain(info):
    label = info[2]
    df = pd.io.sql.read_frame(
        '''
        SELECT `src_id`, DATA, `%s` 
        FROM `src` LEFT JOIN `samples` ON `src`.`id` = `samples`.`src_id`
        WHERE `%s` IS NOT NULL ORDER BY RAND() LIMIT 100
        ''' % (label, label), con
    )
    X = pd.DataFrame(list(df['DATA'].map(lambda x: np.array(pickle.loads(x), dtype=np.float64))))
    y = df[label]

    rf = RF()
    rf.fit(X, y)
    return rf

def getTest(model, info):
    label = info[2]
    df = pd.io.sql.read_frame(
        '''
        SELECT `src`.`id` AS `src_id`, DATA, `%s` 
        FROM `src` LEFT JOIN `samples` ON `src`.`id` = `samples`.`src_id`
        WHERE src.type = 1 AND `%s` IS NULL LIMIT 1000
        ''' % (label, label), con
    )

    X = pd.DataFrame(list(df['DATA'].map(lambda x: np.array(pickle.loads(x), dtype=np.float64))))
    result = model.predict(X)
    df['predict_result'] = result
    df['pid'] = info[0]
    return df.drop(['DATA', label], axis=1)

def putResult(df):
    print df
    pd.io.sql.write_frame(df, 'predict_result', con, flavor = 'mysql', if_exists='append')

info = getOne(5)
model = getTrain(info)
putResult(getTest(model, info))

# print getTrain(getOne(1))
# getOne(2)
# getOne(3)
# getOne(4)
# getOne(5)
