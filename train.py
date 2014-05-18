"""
Train and create prediction.
FIXME: duplicate code with train.py
"""
import pickle
import pandas as pd
import MySQLdb as mdb
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier as RF
import numpy as np
import json

config = json.load(open('config.json'))

con = mdb.connect(config[u'host'], config[u'user'], config[u'password'], config[u'database'])

cur = con.cursor()

cur.execute("SELECT * FROM `predictions` WHERE `id` = '%s' LIMIT 1" % (1))
row = cur.fetchone()

print row
