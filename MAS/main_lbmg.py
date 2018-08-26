import sys
import random
import argparse

from gaussian import gaussian_model

parser = argparse.ArgumentParser()

parser.add_argument('--out_suffix', type=str)
parser.add_argument('--skip', type=int, default=-1)
parser.add_argument('--stdev', type=float, default=0.1)
parser.add_argument('--track_till', type=int, default=1995)
parser.add_argument('--num_threads', type=int, default=4)

args = parser.parse_args()

gaussian_model(args.out_suffix, args.skip, args.stdev, args.track_till, args.num_threads)
