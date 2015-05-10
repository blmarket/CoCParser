#!/usr/bin/env python3
import redis
import boto
from boto.s3.key import Key
import uuid
from urllib.parse import quote_plus
from parse import check_and_parse
from skimage.io import imsave
from io import BytesIO
import tornado.web
import json
import requests

bucket = boto.connect_s3().get_bucket('cocparser')
base_url = 'https://cocparser.s3.amazonaws.com/'

api_key = None
with open("config.json") as conf: # load from module main path
    api_key = json.load(conf)['mailgun']

def __upload(objectId, fp):
    k = Key(bucket)
    k.key = objectId
    k.content_type = 'image/png'
    k.set_contents_from_file(fp, reduced_redundancy = True, rewind = True)
    return base_url + objectId

def process(user, title, files):
    base_path = "v0/" + quote_plus(user) + "/" + quote_plus(title) + "/"
    """
    process files to s3
    """
    for idx, fp in enumerate(files):
        for isEnemy, slit in check_and_parse(fp):
            if isEnemy: continue
            png = BytesIO()
            imsave(png, slit)
            yield __upload(base_path + "slit/" + str(uuid.uuid4()) + ".png", png), slit

def prepare_models():
    import redis, lzma, pickle
    r = redis.StrictRedis(port = 6379)
    def get_model(label):
        model = pickle.loads(lzma.decompress(r.get("model:%s" % label)))
        model.verbose = 0
        return model
    labels = [ 'total_stars', 'clan_place', 'atk_eff1', 'attack1', 'atk_eff2', 'attack2' ]
    return zip(labels, map(get_model, labels)), get_model('number')

def classify(img):
    import skimage.io
    import numpy as np
    from slit_utils import cutfront2

    fl = img.flatten()

    ret = {}

    def predict_with_prob(model, data):
        return sorted(list(np.dstack([ model.classes_, model.predict_proba(img.flatten())[0] ])[0]), key = lambda x: -x[1])[0]

    models, m2 = prepare_models()
    for k, model in models:
        prediction = model.predict(fl.flatten())[0]
        ret[k] = prediction

    a, b = cutfront2(img)
    v1, v2 = map(lambda x: m2.predict(x.flatten())[0], (a,b))
    ret['number1'] = v1
    ret['number2'] = v2
    return ret

def convert_urls(attachments):
    def download_from_mailgun(url):
        response = requests.get(url, auth=('api', api_key))
        return BytesIO(response.content)

    for it in attachments:
        yield download_from_mailgun(it['url'])

def handle_service_task(task):
    for url, slit in process(task['sender'], task['title'], convert_urls(task['attachments'])):
        print(url, classify(slit))

class ServiceHandler(tornado.web.RequestHandler):
    def initialize(self, executor):
        self.executor = executor

    def post(self):
        to = self.get_argument('To')
        sender = self.get_argument('sender')
        attachments = json.loads(self.get_argument('attachments', default='[]'))
        title = self.get_argument('Subject')

        task = {'to': to, 'sender': sender, 'attachments': attachments, 'title': title }
        print("ServiceHandler", json.dumps(task))

        self.executor.submit(handle_service_task, task)

        self.write("OK")

if __name__ == "__main__":
    image_list = [ '5.png' ]
    members = [ (url, classify(slit)) for url, slit in process('blmarket', 'test', map(lambda x: open(x, "rb"), image_list)) ]
    print(members)
