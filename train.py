#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Train and create prediction.
"""
from sys import exit
from io import BytesIO
import sqlalchemy as sa
import pickle
import pandas as pd
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier as RF
from skimage import io
import numpy as np
import json
import engine
import db_mysql

engine = engine.get_engine()

def getTrain(label):
    df = pd.io.sql.read_sql_query(
        '''
        SELECT `src_id`, `value` FROM `tags`
        WHERE `name` = '%s' AND `probability` IS NULL
        ORDER BY `src_id` DESC LIMIT 1200
        ''' % (label), engine
    )

    X = list(df['src_id'].map(lambda x: np.load(BytesIO(db_mysql.cache_mysql(x)))))
    y = df['value']
    if label == 'atk_eff1' or label == 'atk_eff2': # sorry, crappy label check here.
        y = y.map(lambda x: 1 if x != 0 else 0)

    rf = RF(n_estimators = 150, n_jobs = 3, verbose = 1)
    rf.fit(X, y) # 3 is good for usual multicore system
    print("Fit complete")
    return rf

def getPrediction(model, label):
    df = pd.io.sql.read_sql_query('''
    SELECT `src`.`id` as `src_id`
    FROM `src` 
    WHERE `id` NOT IN (SELECT `src_id` FROM `tags` WHERE `name`='%s')
    LIMIT 1000;
    ''' % (label), engine)

    if len(df) == 0:
        return None

    X = pd.DataFrame(list(df['src_id'].map(lambda x: np.load(BytesIO(db_mysql.cache_mysql(x))))))
    result = model.predict(X)
    probs = model.predict_proba(X)

    df['name'] = label
    df['value'] = result
    df['probability'] = map(max, probs)
    print(df)
    return df

def putResult(df):
    pd.io.sql.to_sql(df, 'tags', engine, if_exists='append', index=False)

if __name__ == "__main__":
    for label_name in [ 'clan_place', 'name', 'attack1', 'attack2', 'total_stars', 'atk_eff1', 'atk_eff2' ]:
        print(label_name)
        model = getTrain(label_name)
        prediction = getPrediction(model, label_name)
        if prediction is None:
            continue
        putResult(prediction)
