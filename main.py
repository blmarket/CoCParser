import glob
from itertools import chain
from parse import parse

L = chain.from_iterable(parse(filename) for filename in glob.glob('*.png'))

print L

for it in L:
    print it
