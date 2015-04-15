import engine as e
import redis
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import text
from sqlalchemy import Column, Integer, String, UniqueConstraint, Unicode
from models import *

import skimage.io

Base = declarative_base()

class Effectives(Base):
    __tablename__ = 'eff_atks'
    __table_args__ = (
            UniqueConstraint('date', 'group_id', 'group_idx'),
            )

    id = Column(Integer, primary_key = True)
    date = Column(Unicode(128, collation = 'utf8_general_ci'), nullable = False)
    src_id = Column(Integer, nullable = False)
    atk_id = Column(Integer, nullable = False)
    group_id = Column(Integer, nullable = False)
    group_idx = Column(Integer, nullable = False)

engine = e.get_engine()
r = redis.StrictRedis()

Base.metadata.create_all(engine)

def clear_tags(date):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM eff_atks WHERE date = :date"), date = date)
        conn.execute(text("DELETE FROM tags WHERE name = 'most' AND src_id IN "
            "(SELECT id FROM src WHERE category = :date)"), date = date)

def add_tag(src_id, tag_name, value):
    with engine.connect() as conn:
        conn.execute("INSERT INTO tags (src_id, name, value) VALUES ('%s', '%s', '%s')" % (src_id, tag_name, value))

def compact_json(obj):
    return json.dumps(obj, separators=(',',':'))

def get_mysql(src_id):
    with engine.connect() as conn:
        return conn.execute('SELECT DATA FROM src WHERE id = %s' % src_id).fetchone()[0]

def get_tag_from_mysql(tup):
    src_id, name = tup
    with engine.connect() as conn:
        return conn.execute("SELECT value FROM tags WHERE src_id = '%s' AND name = '%s'" % (src_id, name)).fetchone()[0]

def update_tag_from_mysql(src_id, name, value):
    with engine.connect() as conn:
        conn.execute("UPDATE tags SET value = %s WHERE src_id = %s AND name = '%s'" % (value, src_id, name))

def get_id_list_from_mysql(category):
    with engine.connect() as conn:
        return compact_json(map(lambda x: x[0], conn.execute("SELECT id FROM src WHERE category = '%s'" % category).fetchall()))

def war_index_mysql(category):
    with engine.connect() as conn:
        return compact_json(map(lambda x: x[0], conn.execute("SELECT id FROM war WHERE date = '%s'" % category).fetchall()))

def tag_key_strategy(tup):
    src_id, name = tup
    return 'tag:%s:%s' % (src_id, name)

def src_key_strategy(src_id):
    return 'src:%s' % src_id

def idlist_key_strategy(category):
    return 'ids:%s' % category

def war_index_key_strategy(category):
    return 'war:ids:%s' % category

def cacheFactory(base, key_strategy):
    def func(key):
        redis_key = key_strategy(key)
        val = r.get(redis_key)
        if val: return val
        val = base(key)
        r.set(redis_key, val)
        return val
    return func

cache_mysql = cacheFactory(get_mysql, src_key_strategy)
cache_tag = lambda x, y: cacheFactory(get_tag_from_mysql, tag_key_strategy)((x, y))
cache_attack = lambda (x, y): cache_tag(x, "attack%s" % (y+1))
cache_ids = lambda x: json.loads(cacheFactory(get_id_list_from_mysql, idlist_key_strategy)(x))
cache_war = lambda x: json.loads(cacheFactory(war_index_mysql, war_index_key_strategy)(x))

# singleton session... no...
session = Session(e.get_engine())
def target_rank(war_id):
    tmp = session.query(War).filter(War.id == war_id).one()
    ret = compact_json(map(lambda x: cache_tag(x, 'number'),
            [ tmp.atk1_src, tmp.atk2_src ]))
    return ret

def get_src_from_s3(src_id):
    # url = 'e56e3be6-9f2d-4872-8288-0744ef4fdbf9.png'
    url = session.query(Src).filter(Src.id == src_id).one().data_url
    print skimage.io.imread(url, as_grey = True).flatten()

cache_target_rank = lambda x: json.loads(cacheFactory(target_rank, lambda x: 'trank:%s' % (x)))

if __name__ == "__main__":
    import numpy as np
    from io import BytesIO
    get_src_from_s3(12000)
    print np.load(BytesIO(cache_mysql(12000))).flatten()
