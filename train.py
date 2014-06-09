"""
Train and create prediction.
FIXME: duplicate code with train.py
"""
import sys
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

def getTrain(label):
    df = pd.io.sql.read_frame(
        '''
        SELECT `src_id`, `DATA`, `value` 
        FROM `src` LEFT JOIN `tags` ON `src`.`id` = `tags`.`src_id`
        WHERE `name` = '%s' AND `probability` IS NULL
        ''' % (label), con
    )
    print "REad data complete"
    X = pd.DataFrame(list(df['DATA'].map(lambda x: np.array(pickle.loads(x), dtype=np.float64))))
    y = df['value']

    rf = RF(n_jobs = 3)
    rf.fit(X, y) # 3 is good for usual multicore system
    print "Fit complete"
    return rf

def getPrediction(model, label):
    df = pd.io.sql.read_frame(
        '''
        SELECT `id` AS `src_id`, DATA FROM `src`
        WHERE `type` = '1' AND `id` NOT IN (
            SELECT src_id FROM tags WHERE `name` = '%s'
        ) LIMIT 1000
        ''' % (label), con
    )

    X = pd.DataFrame(list(df['DATA'].map(lambda x: np.array(pickle.loads(x), dtype=np.float64))))
    result = model.predict(X)

    df['name'] = label
    df['value'] = result
    df['probability'] = 0.5
    return df.drop(['DATA'], axis=1)

def putResult(df):
    pd.io.sql.write_frame(df, 'tags', con, flavor = 'mysql', if_exists='append')

for label_name in [ 'clan_place', 'name', 'attack1', 'attack2', 'total_stars' ]:
    model = getTrain(label_name)
    prediction = getPrediction(model, label_name)
    print prediction
    putResult(prediction)

# print getTrain(getOne(1))
# getOne(2)
# getOne(3)
# getOne(4)
# getOne(5)
