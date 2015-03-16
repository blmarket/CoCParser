import flickrapi
from urllib import urlretrieve
import json

# TARGET_TITLE = '20140501'

# Belows informations seems public.(I can't sure for api key.
# even though I didn't exposed its secret key, it doesn't mean
# api key is public information or not, anyway, there is no
# problem of exposing my api key.)
api_key = 'c165ac58362fc00ad075c667ef060dc1'
api_secret = '7f5c05b7d82779ba'
myid = '123519224@N08'

def fetch_images(title):
    fl = flickrapi.FlickrAPI(api_key, api_secret)
    res = fl.photos_search(
            user_id = myid, per_page = '20',
            extras = 'url_o',
            format = 'json')

    photos = json.loads(res)[u'photos']['photo']

    for photo in photos:
        if photo[u'title'] != title:
            continue
        url = photo[u'url_o']
        yield url

def download_images(title):
    urls = list(fetch_images(title))
    for i in range(len(urls)):
        url = urls[i]
        urlretrieve(url, "%d.png" % (i))

if __name__ == "__main__":
    # 1. download them
    download_images('20150316')
    # 2. list images
    # for it in fetch_images('20140501'):
    #     print it
