import sys
import random
import argparse
#from multiprocessing.dummy import Pool
from multiprocessing import Pool
import math

from loc import location_model

parser = argparse.ArgumentParser()

parser.add_argument('--out_suffix', type=str)
parser.add_argument('--gamma', type=str)
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

if args.gamma == 'log':
	location_model(args.out_suffix, args.track_till, math.log, args.num_threads)
elif args.gamma == 'linear':
	location_model(args.out_suffix, args.track_till, lambda x: x, args.num_threads)
elif args.gamma == 'sqrt':
	location_model(args.out_suffix, args.track_till, math.sqrt, args.num_threads)
elif args.gamma == 'constant':
	location_model(args.out_suffix, args.track_till, lambda x: x*0 + 5, args.num_threads)
