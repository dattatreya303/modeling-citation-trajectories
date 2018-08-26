# code to simulate the growth model of a citation network
# Location-based model

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
from multiprocessing.dummy import Pool as ThreadPool

def location_model(out_suffix, track_till, gamma_fn, num_threads):
	
	fit_x = lambda size: np.random.pareto(1,size)
	alpha = lambda l1, l2, gam: np.exp( -1 * gam * norm(l1-l2) )
	beta = lambda f,d: f*d
	
	t = 0	# time counter
	
	# loading initial graph generated from real data
	file_name = 'newData_initial_graph'
	g = nx.read_adjlist('./'+file_name, create_using=nx.DiGraph())
	print 'initial graph: nodes:',len(g.nodes()),', edges:',len(g.edges())
	
	# Creating a node:[edges] dictionary.
	node_edges_dict = dict()
	with open('node_edges_dict') as f:
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
	
	# Assigning fitness attributes for each paper
	for paper in g.nodes():
		g.node[paper]['fitness'] = fit_x(1)[0]
		g.node[paper]['location'] = np.random.uniform(0,1,2)
	
	node_beta_values = { x: beta(g.in_degree(x)+1,g.node[x]['fitness']) for x in g.nodes() }

	uni = 0
	
	try:
			# Sorting nodes according to the year in which they appeared.
			nodes_by_year = sorted(node_year_dict.keys(), key = lambda x: int(node_year_dict[str(x)]) )
			
			i = 0
			curYear = end_year
			newEdges = []
			
			for newNode in nodes_by_year:
	
				i += 1
	
				if int(node_year_dict[newNode]) <= end_year:
					continue
				
				if int(node_year_dict[newNode]) > track_till:
					break
				
				# Changing year.
				if int(node_year_dict[newNode]) != curYear:
					t = t + ( int(node_year_dict[newNode]) - curYear)
					print("gauss ********* {0} *********".format(t))
					curYear = int(node_year_dict[newNode])
	
				k = -1
				try:
					k = len(node_edges_dict[newNode])
				except KeyError as ke:
					# If node has no references in real data.
					continue
					
				newFit = fit_x(1)[0]
				newLoc = np.random.uniform(0,1,2)
	
				j = 0
				newEdges[:] = []
				# node_link_probs = [ [ alpha(g.node[x]['location'],newLoc,math.log(g.number_of_nodes())) * beta(g.in_degree(x)+1,g.node[x]['fitness']), x ] for x in g.nodes()]
				node_link_probs = [ [ alpha(g.node[x]['location'],newLoc,gamma_fn(g.number_of_nodes())) * node_beta_values[x], x ] for x in g.nodes()]
				#node_link_probs = threadpool.map(lambda x: get_link_probs(g, x, g.number_of_nodes(), node_beta_values), g.nodes())
				# print(link_probs[:, 0])
				link_probs = np.array([l[0] for l in node_link_probs])
				sum_probs = np.sum(link_probs)
				# link_probs = [ l[0]/float(sum_probs) for l in link_probs ]
				link_probs = link_probs / float(sum_probs)
				
				try:
					newEdges = list(np.random.choice([ l[1] for l in node_link_probs ], k, False, link_probs))
				except Exception as e:
					newEdges = list(np.random.choice([ l[1] for l in node_link_probs ], k, False))				
					uni += 1
				
				g.add_node( newNode, fitness=newFit, location=newLoc )
				node_beta_values[newNode] = beta(g.in_degree(newNode)+1,g.node[newNode]['fitness'])
	
				for newDest in newEdges:
					g.add_edge(newNode, newDest)
					g.edge[newNode][newDest]['year'] = t
					node_beta_values[newDest] = beta(g.in_degree(newDest)+1,g.node[newDest]['fitness'])
					
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
	print out_suffix, 'final graph: nodes:',len(g.nodes()),', edges:',len(g.edges()), uni
	
