"""
Creates web-public image url for given image blob.
"""
from itertools import chain
from parse import parse
import pickle
import MySQLdb as mdb
import sqlite3
from flickr import fetch_images
from StringIO import StringIO
from skimage import io

import boto
from boto.s3.key import Key

import uuid

conn = boto.connect_s3()
bucket = conn.get_bucket('cocparser')

def createBlob(png_chunk):
    objectId = title + '/' + str(uuid.uuid4()) + '.png'

    k = Key(bucket)
    k.key = objectId
    k.content_type = 'image/png'
    k.set_contents_from_string(png_chunk)

    url = 'https://cocparser.s3.amazonaws.com/' + objectId
    return url
