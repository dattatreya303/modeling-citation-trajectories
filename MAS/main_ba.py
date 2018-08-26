import sys
import random
import argparse
#from multiprocessing.dummy import Pool
from multiprocessing import Pool

from ba import ba_model

parser = argparse.ArgumentParser()

#parser.add_argument('--opt_file', type=str, default=None)

parser.add_argument('--out_suffix', type=str)
parser.add_argument('--track_till', type=int, default=1995)
parser.add_argument('--num_threads', type=int, default=4)

args = parser.parse_args()

"""
opts = []
with open(args.opt_file) as f:
	opts = f.readlines()
opts = [l.strip().split(' ') for l in opts]
opts = [[l[0], int(l[1]), float(l[2]), int(l[3]), int(l[4])] for l in opts]

pool = Pool(24)
pool.map(lambda x:gaussian_model(*x), opts)
pool.close()
pool.join()
"""

ba_model(args.out_suffix, args.track_till, args.num_threads)
