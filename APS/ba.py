
# code to simulate the growth model of a citation network
# Location-based model, with varying gaussian locations, 

import networkx as nx
import numpy as np
import itertools
import math
from math import exp
from numpy.linalg import norm
import sys
import random
from matplotlib import pyplot as plt
import json
import argparse

def ba_model(out_suffix, track_till, num_threads):

	fit_x = lambda size: np.random.pareto(1,size)

	t = 0	# time counter

	# loading initial graph generated from real data
	start_year = 1960
	end_year = 1965
	file_name = 'aps_initial_graph_'+str(start_year)+'_'+str(end_year)
	g = nx.read_adjlist('./'+file_name, create_using=nx.DiGraph())
	print 'initial graph: nodes:',len(g.nodes()),', edges:',len(g.edges())

	# Creating a node:[edges] dictionary.
	node_edges_dict = dict()
	with open('node_edge_dict') as f:
		node_edges_dict = json.load(f)

	# Creating a node:year dictionary.
	node_year_dict = dict()
	with open('node_year_dict') as f:
		node_year_dict = json.load(f)

	# Creating a year:nodes dictionary.
	year_node_dict = dict()
	with open('year_node_dict') as f:
		year_node_dict = json.load(f)

	# initializing year attributes for each citation
	for citation in g.edges():
		g.edge[citation[0]][citation[1]]['year'] = 0

	#exit(0)

	try:
			# Sorting nodes according to the year in which they appeared.
			nodes_by_year = sorted(node_year_dict.keys(), key = lambda x: int(node_year_dict[str(x)]) )
			
			# for i in range(10):
			# 	print(nodes_by_year[i], node_year_dict[nodes_by_year[i]])

			i = 0
			newEdges = []
			curYear = end_year
			
			for newNode in nodes_by_year:

				# print("...... {0} ......".format(len(deg_roulette)))

				i += 1
				#print(i)

				if int(node_year_dict[newNode]) <= end_year:
					continue
				
				if int(node_year_dict[newNode]) > track_till + 10:
					break
				
				# Changing year.
				if int(node_year_dict[newNode]) != curYear:
					t = t + ( int(node_year_dict[newNode]) - curYear)
					print("********* {0} *********".format(t))
					curYear = int(node_year_dict[newNode])

				k = -1
				try:
					k = len(node_edges_dict[newNode])
				except KeyError as ke:
					# If node has no references in real data.
					continue
					
				newFit = fit_x(1)[0]

				# print('**',k)
				j = 0
				# pas = 0
				newEdges[:] = []
				node_link_probs = [ (g.in_degree(x) + 0.1, x ) for x in g.nodes()]

				link_probs = np.array([l[0] for l in node_link_probs])
				sum_probs = np.sum(link_probs)
				# link_probs = [ l[0]/float(sum_probs) for l in link_probs ]
				link_probs = link_probs / float(sum_probs)
				
				newEdges = list(np.random.choice([ l[1] for l in node_link_probs ], k, False, link_probs))
				
				g.add_node( newNode, fitness=newFit)

				for newDest in newEdges:
					g.add_edge(newNode, newDest)
					g.edge[newNode][newDest]['year'] = t

				#print(g.number_of_nodes(), g.number_of_edges())
									
	except KeyboardInterrupt as e:
		#exit(0)
		pass


	# saving network in the form of an edge list
	out_papers = './AllPapersSim_' + out_suffix
	out_edges = './TemporalEdgeListSim_' + out_suffix
	f = open(out_papers, 'wb')
	for paper in g.nodes():
		f.write(str(paper)+'\n')
	f.close()
	f = open(out_edges, 'wb')
	for citation in g.edges():
		# print(g.edge[citation[0]][citation[1]]['year'])
		f.write(str(citation[0])+'\t'+str(citation[1])+'\t'+str(g.edge[citation[0]][citation[1]]['year'])+'\n')
		pass
	f.close()
	print 'final graph: nodes:',len(g.nodes()),', edges:',len(g.edges())
