import flickrapi
from urllib import urlretrieve

TARGET_TITLE = '20140418'

# Belows informations seems public.(I can't sure for api key.
# even though I didn't exposed its secret key, it doesn't mean
# api key is public information or not, anyway, there is no
# problem of exposing my api key.)
api_key = 'c165ac58362fc00ad075c667ef060dc1'
myid = '123519224@N08'

fl = flickrapi.FlickrAPI(api_key)
res = fl.photos_search(user_id = myid, text=TARGET_TITLE, per_page = '20', format = 'etree', extras = 'url_o')

photos = res.find('photos').findall('photo')

for i in range(len(photos)):
    photo = photos[i]
    url = dict(photo.items())['url_o']
    print url
    urlretrieve(url, "%d.png" % (i))
