#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Train and create prediction.
"""
from sys import exit
from StringIO import StringIO
import sqlalchemy as sa
import pickle
import pandas as pd
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier as RF
from skimage import io
import numpy as np
import json
import engine

engine = engine.get_engine()

def getTrain(label):
    df = pd.io.sql.read_sql_query(
        '''
        SELECT `src_id`, `DATA`, `value` 
        FROM `src` LEFT JOIN `tags` ON `src`.`id` = `tags`.`src_id`
        WHERE `name` = '%s' AND `probability` IS NULL
        ORDER BY `src`.`id` DESC LIMIT 800
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
    df = pd.io.sql.read_sql_query(
        '''
        SELECT `id` AS `src_id`, DATA FROM `src`
        WHERE `type` = '1' AND `id` NOT IN (
            SELECT src_id FROM tags WHERE `name` = '%s'
        ) LIMIT 1000
        ''' % (label), engine
    )

    if len(df) == 0:
        return None

    X = pd.DataFrame(list(df['DATA'].map(lambda x: np.load(StringIO(x)))))
    result = model.predict(X)
    probs = model.predict_proba(X)

    df['name'] = label
    df['value'] = result
    df['probability'] = map(max, probs)
    return df.drop(['DATA'], axis=1)

def putResult(df):
    pd.io.sql.to_sql(df, 'tags', engine, if_exists='append')

for label_name in [ 'clan_place', 'name', 'attack1', 'attack2', 'total_stars' ]:
    print label_name
    model = getTrain(label_name)
    prediction = getPrediction(model, label_name)
    if prediction is None:
        continue
    putResult(prediction)
