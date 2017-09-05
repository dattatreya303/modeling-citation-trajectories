# code to simulate the growth model of a citation network
# Barabasi-Albert model

import networkx as nx
import numpy as np
import itertools
from math import exp
from numpy.linalg import norm
import sys
import random
from matplotlib import pyplot as plt
import json

fit_x = lambda x: np.random.pareto(1,x)

t = 0	# time counter

# loading initial graph generated from real data
start_year = 1960
end_year = 1975
file_name = 'newData_initial_graph_'+str(start_year)+'_'+str(end_year)
g = nx.read_adjlist('./'+file_name, create_using=nx.DiGraph())
print 'initial graph: nodes:',len(g.nodes()),', edges:',len(g.edges())

# initializing year attributes for each citation
for citation in g.edges():
	g.edge[citation[0]][citation[1]]['year'] = t

# Assigning fitness attributes for each paper
for paper in g.nodes():
	g.node[paper]['fitness'] = int( fit_x(1)[0] )
	g.node[paper]['strength'] = g.in_degree(paper) + g.node[paper]['fitness']
	print(g.node[paper]['fitness'], g.node[paper]['strength'])

exit(0)

try:
		# Creating a node:[edges] dictionary.
		node_edges_dict = dict()
		with open('node_edges_dict') as f:
			node_edges_dict = json.load(f)
		
		# Creating a node:year dictionary..
		node_year_dict = dict()
		with open('node_year_dict') as f:
			node_year_dict = json.load(f)
		
		# Sorting nodes according to the year in which they appeared.
		nodes_by_year = sorted(node_year_dict.keys(), key = lambda x: int(node_year_dict[str(x)]) )

		# Creating a degree:[nodes] dictionary.
		# Min. degree of a node will be 1. Node having no citations will be taken care of later.
		stren_nodes_dict = dict()
		for paper in g.nodes():
			stren = g.node[paper]['strength']
			if stren not in stren_nodes_dict.keys():
				stren_nodes_dict[stren] = set()
			stren_nodes_dict[stren].add( paper )

		# Creating a roulette field for node degrees.
		stren_roulette = list()
		for s in sorted(stren_nodes_dict.keys()):
			if len(stren_nodes_dict[s]) > 0:
				stren_roulette.extend( [s] * s )
		
		i = 0
		newEdges = []
		curYear = end_year
		sumDegree = 2 * g.number_of_edges()
		for newNode in nodes_by_year:

			i += 1
			print(i)

			if int(node_year_dict[newNode]) <= end_year:
				continue
			
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

			j = 0
			# pas = 0
			newEdges[:] = []
			while j < k:

				"""
				Roulette selection of random node using preferential attachment.
				"""
				
				# Choose a random index from roulette field.
				rand = random.randint( 0, len(stren_roulette) - 1 )
				# Degree of the index chosen.
				ch_deg = int( stren_roulette[rand] )
				print('**Deg', ch_deg)
				# Choose a random node having that degree in the existing network.
				randNode = random.choice( tuple( stren_nodes_dict[ch_deg] ) )
				
				# Remove that newNode from further selections.
				stren_nodes_dict[ch_deg].remove( randNode )
				if len( stren_nodes_dict[ch_deg] ) == 0:
					# Remove that degree from roulette field, if no nodes having that degree exist in the network.
					stren_roulette = [ el for el in stren_roulette if el != ch_deg ]

				"""
				Tuple of (destNode, newDegree).
				Will be added to graph after all edges have been decided.
				"""
				# If node has 0 in-degree, it should be placed in degree 1 list again as it has 1 ciatation now.
				if g.in_degree(randNode) == 0:
					newEdges.append( (randNode, 1) )
				else:
					newEdges.append( (randNode, ch_deg+1) )
				j += 1

			for e in newEdges:
				g.add_edge(newNode, e[0])
				g.edge[newNode][e[0]]['year'] = t

				# Update degree dictionary.
				if e[1] not in stren_nodes_dict.keys() or len(stren_nodes_dict[e[1]]) == 0:
					stren_nodes_dict[e[1]] = set()
					stren_roulette.extend( [int(e[1])] * int(e[1]) )
				stren_nodes_dict[ e[1] ].add(e[0])
			
			# Keep degree of new node as 1, so that it is available for further roulette selections.
			g.node[newNode]['fitness'] = int( fit_x(1) )
			g.node[newNode]['strength'] = 1 + g.node[newNode]['fitness']
			newNodeStren = g.node[newNode]['strength']
			if newNodeStren not in stren_nodes_dict.keys() or len(stren_nodes_dict[ newNodeStren ]) == 0:
				stren_nodes_dict[ newNodeStren ] = set()
				stren_roulette.extend( [ newNodeStren ] * newNodeStren )
			stren_nodes_dict[ newNodeStren ].add(newNode)
			
			# Shuffle the roulette field.
			random.shuffle(stren_roulette)
			
			print(g.number_of_nodes(), g.number_of_edges())

except KeyboardInterrupt as e:
	pass


# saving network in the form of an edge list
out_papers = './AllPapersSim_fromNew'
out_edges = './TemporalEdgeListSim_fromNew'
f = open(out_papers, 'wb')
for paper in g.nodes():
	f.write(str(paper)+'\n')
f.close()
f = open(out_edges, 'wb')
for citation in g.edges():
	f.write(str(citation[0])+'\t'+str(citation[1])+'\t'+str(g.edge[citation[0]][citation[1]]['year'])+'\n')
	pass
f.close()
print 'final graph: nodes:',len(g.nodes()),', edges:',len(g.edges())
