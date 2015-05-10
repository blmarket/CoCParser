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
from sklearn.ensemble import RandomForestClassifier as RF
from skimage import io
import numpy as np
import json
from models import engine, db_mysql
import concurrent.futures

engine = engine.get_engine()

def getTrain(label):
    df = pd.io.sql.read_sql_query(
        '''
        SELECT `data_url`, `value` FROM `tags`
        LEFT JOIN `src` ON `src_id` = `src`.`id`
        WHERE `name` = '%s' AND `probability` IS NULL
        ORDER BY `src_id` DESC LIMIT 1800
        ''' % (label), engine
    )

    def dbg(x):
        print(x)
        return np.load(BytesIO(db_mysql.cache_src(x))).flatten()

    X = None
    with concurrent.futures.ThreadPoolExecutor(max_workers = 4) as e:
        X = pd.DataFrame(list(e.map(dbg, df['data_url'])))

    y = df['value']

    rf = RF(n_estimators = 150, n_jobs = 3, verbose = 1)
    rf.fit(X, y) # 3 is good for usual multicore system
    print("Fit complete")
    return rf

def getPrediction(model, label, source_types):
    where_clause = " AND src.type IN %s " % (source_types)

    print(where_clause)

    df = pd.io.sql.read_sql_query('''
    SELECT `src`.`id` as `src_id`, `data_url`
    FROM `src` 
    WHERE `id` NOT IN (SELECT `src_id` FROM `tags` WHERE `name`='%s') %s
    LIMIT 1000;
    ''' % (label, where_clause), engine)

    if len(df) == 0:
        return None

    X = pd.DataFrame(list(df['data_url'].map(lambda x: np.load(BytesIO(db_mysql.cache_src(x))).flatten())))
    result = model.predict(X)
    probs = model.predict_proba(X)

    df['name'] = label
    df['value'] = result
    df['probability'] = list(map(max, probs))
    df.drop('data_url', axis=1, inplace=True)
    print(df)
    return df

def putResult(df):
    pd.io.sql.to_sql(df, 'tags', engine, if_exists='append', index=False)

if __name__ == "__main__":
    import redis, lzma
    r = redis.StrictRedis(port = 6379)
    for label_name in [ 'name', 'clan_place', 'attack1', 'attack2', 'total_stars', 'atk_eff1', 'atk_eff2', 'number' ]:
        print(label_name)

        # r.set("model:%s" % label_name, lzma.compress(pickle.dumps(getTrain(label_name))))
        model = pickle.loads(lzma.decompress(r.get("model:%s" % label_name)))

        ## crappy case handling...
        where_clause = "( '1','2' )"
        if label_name == 'name':
            where_clause = "( '1' )"
        if label_name == 'number':
            where_clause = "( '3' )"

        prediction = getPrediction(model, label_name, where_clause)
        if prediction is None:
            continue
        putResult(prediction)

