import flickrapi
from sys import exit
import redis
import time
import json
from parse import parse
from write_src import write_src

api_key = 'c165ac58362fc00ad075c667ef060dc1'
r = redis.StrictRedis()
fl = flickrapi.FlickrAPI(api_key)

def photoUrl(photo_id):
    res = fl.photos_getInfo(photo_id = photo_id)
    photo = res.find('photo')
    dic = dict(photo.items())

    url = 'http://farm%s.static.flickr.com/%s/%s_%s_o.png' % (
            dic['farm'], dic['server'], dic['id'], dic['originalsecret'])
    return url

while True:
    if r.llen('flickr') == 0:
        print 'Empty queue!'
        exit(0)
    obj = json.loads(r.lpop('flickr'))
    try:
        for it in obj[u'items']:
            photo_id = it[u'id'].split('/')[-1]
            title = it[u'title']
            url = photoUrl(photo_id)
            write_src(parse(url), title)
    except Exception as e:
        print obj
        raise e

