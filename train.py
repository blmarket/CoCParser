#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Train and create prediction.
FIXME: duplicate code with train.py
"""
from sys import exit
from StringIO import StringIO
import sqlalchemy as sa
import pickle
import pandas as pd
import MySQLdb as mdb
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier as RF
from skimage import io
import numpy as np
import json

config = None
with open('config.json') as conf:
    config = json.load(conf)

if not config:
    exit(-1)

conn_str = "mysql://%s:%s@%s/%s" % (config[u'user'], config[u'password'], config['host'], config['database'])

engine = sa.create_engine(conn_str, encoding = 'utf8')

def getTrain(label):
    df = pd.io.sql.read_sql(
        '''
        SELECT `src_id`, `DATA`, `value` 
        FROM `src` LEFT JOIN `tags` ON `src`.`id` = `tags`.`src_id`
        WHERE `name` = '%s' AND `probability` IS NULL
        ''' % (label), engine
    )
    print df
    print "REad data complete"

    X = pd.DataFrame(list(df['DATA'].map(lambda x: np.load(StringIO(x)))))
    y = df['value']

    rf = RF(n_jobs = 3)
    rf.fit(X, y) # 3 is good for usual multicore system
    print "Fit complete"
    return rf

def getPrediction(model, label):
    df = pd.io.sql.read_sql(
        '''
        SELECT `id` AS `src_id`, DATA FROM `src`
        WHERE `type` = '1' AND `id` NOT IN (
            SELECT src_id FROM tags WHERE `name` = '%s'
        ) LIMIT 1000
        ''' % (label), engine
    )
    
    print len(df)

    if len(df) == 0:
        return None

    X = pd.DataFrame(list(df['DATA'].map(lambda x: np.load(StringIO(x)))))
    result = model.predict(X)

    df['name'] = label
    df['value'] = result
    df['probability'] = 0.5
    return df.drop(['DATA'], axis=1)

def putResult(df):
    pd.io.sql.write_frame(df, 'tags', engine, flavor = 'mysql', if_exists='append')

for label_name in [ 'clan_place', 'name', 'attack1', 'attack2', 'total_stars' ]:
    model = getTrain(label_name)
    prediction = getPrediction(model, label_name)
    if prediction is None:
        continue
    print prediction
    putResult(prediction)
