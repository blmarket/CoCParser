import numpy as np
from skimage import io
from sys import exit
import pyocr
from PIL import Image

FILENAME = 'test.png'

tool = None

tools = pyocr.get_available_tools()
if len(tools) == 0:
    exit(-1)
tool = tools[0]

lang = 'eng'

img = Image.open(FILENAME)
ff = io.imread(FILENAME)

txt = tool.image_to_string(img,
                     lang = lang,
                     builder = pyocr.builders.TextBuilder())

word_boxes = tool.image_to_string(img,
                                  lang=lang,
                                  builder=pyocr.builders.WordBoxBuilder())

for it in word_boxes:
    ((a,b),(c,d)) = it.position
    io.imshow(ff[b:d, a:c])
