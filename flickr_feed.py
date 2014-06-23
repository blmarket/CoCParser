import urllib2
import json

url = 'https://api.flickr.com/services/feeds/photos_public.gne?id=123519224@N08&format=json&nojsoncallback=1'

fp = urllib2.urlopen(url)
tmp = json.load(fp)
for it in tmp[u'items']:
    print it.keys()
    print it[u'title']
    print it[u'published']
