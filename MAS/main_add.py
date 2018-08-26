import sys
import random
import argparse

from add import additive_fitness_model

parser = argparse.ArgumentParser()

parser.add_argument('--out_suffix', type=str)
parser.add_argument('--track_till', type=int, default=1995)
parser.add_argument('--num_threads', type=int, default=4)

args = parser.parse_args()

additive_fitness_model(args.out_suffix, args.track_till, args.num_threads)
