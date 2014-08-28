import engine as e
import redis

engine = e.get_engine()
r = redis.StrictRedis()

def get_mysql(src_id):
    with engine.connect() as conn:
        return conn.execute('SELECT DATA FROM src WHERE id = %s' % src_id).fetchone()[0]

def redis_key(src_id):
    return 'src:%s' % src_id

def get_redis(src_id):
    return r.get(redis_key(src_id))

def set_redis(src_id, value):
    r.set(redis_key(src_id), value)

def cacheFactory(func):
    def ret(src_id):
        val = get_redis(src_id)
        if val: return val
        val = func(src_id)
        set_redis(src_id, val)
        return val
    return ret

cache_mysql = cacheFactory(get_mysql)

if __name__ == "__main__":
    # print get_redis(588)
    # print get_mysql(588)
    print len(cache_mysql(588))
