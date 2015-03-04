import sqlalchemy as sa
import json

config = None
with open('../config.json') as conf:
    config = json.load(conf)

if not config:
    exit(-1)

conn_str = "mysql+oursql://%s:%s@%s/%s" % (config[u'user'], config[u'password'], config['host'], config['database'])

engine = sa.create_engine(conn_str, encoding = 'utf8')

def get_engine():
    return engine
