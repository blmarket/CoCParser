from sys import exit
import sqlalchemy as sa
import json
import pickle
import numpy as np
from StringIO import StringIO
import sqlsoup

config = None
with open('config.json') as conf:
    config = json.load(conf)

if not config:
    exit(-1)

conn_str = "mysql://%s:%s@%s/%s" % (config[u'user'], config[u'password'], config['host'], config['database'])

engine = sa.create_engine(conn_str, encoding = 'utf8')
db = sqlsoup.SQLSoup(engine)

engine = sa.create_engine(conn_str, encoding = 'utf8')

while True:
    conn = engine.connect()
    rp = conn.execute('SELECT id, data FROM src WHERE id NOT IN (SELECT src_id FROM new_src_data) LIMIT 5')

    for it in rp:
        fp = StringIO()
        np.save(fp, np.array(pickle.loads(it['data'])))
        print it['id'], len(fp.getvalue())
        db.new_src_data.insert(src_id=it['id'], data=str(fp.getvalue()))
        db.commit()

# rp = conn.execute('SELECT data FROM src WHERE id NOT IN (SELECT src_id FROM new_src_data) LIMIT 1').fetchall()
# 
# print np.array(pickle.loads(rp[0]['data']))
