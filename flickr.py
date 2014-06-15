import flickrapi
from urllib import urlretrieve

# TARGET_TITLE = '20140501'

# Belows informations seems public.(I can't sure for api key.
# even though I didn't exposed its secret key, it doesn't mean
# api key is public information or not, anyway, there is no
# problem of exposing my api key.)
api_key = 'c165ac58362fc00ad075c667ef060dc1'
myid = '123519224@N08'

def fetch_images(title):
    fl = flickrapi.FlickrAPI(api_key)
    res = fl.photos_search(user_id = myid, text=title, per_page = '20', format = 'etree', extras = 'url_o')

    photos = res.find('photos').findall('photo')

    for i in range(len(photos)):
        photo = photos[i]
        url = dict(photo.items())['url_o']
        yield url

def download_images(title):
    urls = list(fetch_images(title))
    for i in range(len(urls)):
        url = urls[i]
        urlretrieve(url, "%d.png" % (i))

if __name__ == "__main__":
    # 1. download them
    download_images('20140614')
    # 2. list images
    # for it in fetch_images('20140501'):
    #     print it
