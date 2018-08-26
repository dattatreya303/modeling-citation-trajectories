
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
from multiprocessing.dummy import Pool as ThreadPool

def gaussian_model(out_suffix, skip, stdev, track_till, num_threads):
	
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
	
	def add_new_edges(g, newNode, newDest, t, node_beta_values):
		g.add_edge(newNode, newDest)
		g.edge[newNode][newDest]['year'] = t
		node_beta_values[newDest] = beta(g.in_degree(newDest)+1,g.node[newDest]['fitness'])
	
	def get_link_probs(g, x, num_nodes, node_beta_values):
		return [ alpha(g.node[x]['location'],newLoc,math.log(g.number_of_nodes())) * node_beta_values[x], x ]
	
	#threadpool = ThreadPool(args.num_threads)
	
	try:
			# Sorting nodes according to the year in which they appeared.
			nodes_by_year = sorted(node_year_dict.keys(), key = lambda x: int(node_year_dict[str(x)]) )
			
			i = 0
			newEdges = []
			curYear = end_year
			skipVal = skip
			
			cattr = [ [0.5,0.5], stdev ]
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
					if skip < 0:
						skipVal = max( (-skip) * len(year_node_dict[str(curYear)]) / 12, 1 )
	
				k = -1
				try:
					k = len(node_edges_dict[newNode])
				except KeyError as ke:
					# If node has no references in real data.
					continue
					
				newFit = fit_x(1)[0]
				newLoc = np.random.normal( cattr[0], cattr[1] )
	
				j = 0
				newEdges[:] = []
				# node_link_probs = [ [ alpha(g.node[x]['location'],newLoc,math.log(g.number_of_nodes())) * beta(g.in_degree(x)+1,g.node[x]['fitness']), x ] for x in g.nodes()]
				node_link_probs = [ [ alpha(g.node[x]['location'],newLoc,math.log(g.number_of_nodes())) * node_beta_values[x], x ] for x in g.nodes()]
				#node_link_probs = threadpool.map(lambda x: get_link_probs(g, x, g.number_of_nodes(), node_beta_values), g.nodes())
				# print(link_probs[:, 0])
				link_probs = np.array([l[0] for l in node_link_probs])
				sum_probs = np.sum(link_probs)
				# link_probs = [ l[0]/float(sum_probs) for l in link_probs ]
				link_probs = link_probs / float(sum_probs)
				
				#print(g.nodes())
				#exit(0)
				# while j < k:
	
				# 	# max_deg = g.in_degree( max(g.in_degree(), key = lambda x: g.in_degree(x)) )
				# 	# [ max_deg = g.in_degree(p) for p in g.nodes() if g.in_degree(p) > max_deg ]
	
				# 	"""
				# 	Roulette selection of random node using preferential attachment.
				# 	"""
					
				# 	total_sum = sum( [ l[0] for l in link_probs ] )
				# 	randV = np.random.uniform(0,total_sum)
				# 	curSum = 0
				# 	li = 0
				# 	while curSum < randV:
				# 		curSum += link_probs[li][0]
				# 		li += 1
				# 	li = max(0,li-1)
				# 	pnode = link_probs[li][1]
					
				# 	link_probs = [ l for l in link_probs if l[1] != pnode ]
	
				# 	"""
				# 	Tuple of (destNode, newDegree).
				# 	Will be added to graph after all edges have been decided.
				# 	"""
					
				# 	newEdges.append( pnode )
				# 	j += 1
				# 	# exit(0)
				# 	# pas += 1
	
				newEdges = list(np.random.choice([ l[1] for l in node_link_probs ], k, False, link_probs))
				
				g.add_node( newNode, fitness=newFit, location=newLoc )
				node_beta_values[newNode] = beta(g.in_degree(newNode)+1,g.node[newNode]['fitness'])
	
				for newDest in newEdges:
					g.add_edge(newNode, newDest)
					g.edge[newNode][newDest]['year'] = t
					node_beta_values[newDest] = beta(g.in_degree(newDest)+1,g.node[newDest]['fitness'])
				# threadpool.map(lambda x:add_new_edges(g, newNode, x, t, node_beta_values), newEdges)
				
				# print(g.number_of_nodes(), g.number_of_edges())
				
				if i % skipVal == 0:
					
					var = math.log(g.number_of_nodes()) / float(10)
					m_new = np.random.normal(loc=cattr[0], scale=var**(0.5))
					cattr[0] = m_new
					
	except KeyboardInterrupt as e:
		#exit(0)
		pass
	
	#threadpool.close()
	
	# saving network in the form of an edge list
	out_papers = './AllPapersSim_fromNew_' + out_suffix
	out_edges = './TemporalEdgeListSim_fromNew_' + out_suffix
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
	
