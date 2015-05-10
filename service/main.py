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

def __upload(objectId, fp):
    k = Key(bucket)
    k.key = objectId
    k.content_type = 'image/png'
    k.set_contents_from_file(fp, reduced_redundancy = True, rewind = True)
    return base_url + objectId

def process(task_id, file_path):
    base_path = "v0/" + task_id + "/"
    """
    process files to s3
    """

    k = Key(bucket)
    k.key = base_path + "source.png"
    k.content_type = 'image/png' # TODO: use mime from task itself(at least web server knows)
    k.set_contents_from_filename(file_path)

    for isEnemy, slit in check_and_parse(file_path):
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
    return list(zip(labels, map(get_model, labels))), get_model('number')

models, model_number = prepare_models()

def classify(img):
    import skimage.io
    import numpy as np
    from slit_utils import cutfront2

    fl = img.flatten()

    ret = {}

    def predict_with_prob(model, data):
        return sorted(list(np.dstack([ model.classes_, model.predict_proba(img.flatten())[0] ])[0]), key = lambda x: -x[1])[0]

    for k, model in models:
        prediction = model.predict(fl.flatten())[0]
        ret[k] = prediction

    a, b = cutfront2(img)
    v1, v2 = map(lambda x: model_number.predict(x.flatten())[0], (a,b))
    ret['number1'] = v1
    ret['number2'] = v2
    return ret

if __name__ == "__main__":
    image_list = [ '5.png' ]
    members = [ (url, classify(slit)) for url, slit in process('blmarket', 'test', map(lambda x: open(x, "rb"), image_list)) ]
    print(members)
