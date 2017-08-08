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
		deg_nodes_dict = dict()
		for node in g.nodes():
			deg = g.in_degree(node)
			if deg not in deg_nodes_dict.keys():
				deg_nodes_dict[deg] = set()
			deg_nodes_dict[deg].add( node )

		# Creating a roulette field for node degrees.
		deg_roulette = list()
		for d in sorted(deg_nodes_dict.keys()):
			if len(deg_nodes_dict[d]) > 0:
				for i in range(d):
					deg_roulette.append(d)

		i = 0
		newEdges = []
		curYear = end_year
		for node in nodes_by_year:

			i += 1
			print(i)

			if int(node_year_dict[node]) <= end_year:
				continue
			
			# Changing year.
			if int(node_year_dict[node]) != curYear:
				t = t + ( int(node_year_dict[node]) - curYear)
				print("********* {0} *********".format(t))
				curYear = int(node_year_dict[node])

			k = -1
			try:
				k = len(node_edges_dict[node])
			except KeyError as ke:
				# If node has no references in real data.
				continue

			j = 0
			newEdges[:] = []
			while j < k:

				"""
				Roulette selection of random node using preferential attachment.
				"""
				# Choose a random index from roulette field.
				rand = random.randint( 0, len(deg_roulette) - 1 )
				# Degree of the index chosen.
				ch_deg = int( deg_roulette[rand] )
				# Choose a random node having that degree in the existing network.
				randNode = random.choice( tuple( deg_nodes_dict[ch_deg] ) )
				# Remove that node from further selections.
				deg_nodes_dict[ch_deg].remove( randNode )
				if len( deg_nodes_dict[ch_deg] ) == 0:
					# Remove that degree from roulette field, if no nodes having that degree exist in the network.
					deg_roulette = [ el for el in deg_roulette if el != ch_deg ]
				
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
				g.add_edge(node, e[0])
				g.edge[node][e[0]]['year'] = t

				# Update degree dictionary.
				if e[1] not in deg_nodes_dict.keys() or len(deg_nodes_dict[e[1]]) == 0:
					deg_nodes_dict[e[1]] = set()
					deg_roulette.extend( [int(e[1])] * int(e[1]) )
				deg_nodes_dict[ e[1] ].add(e[0])
			
			# Keep degree of new node as 1, so that it is available for further roulette selections.
			if 1 not in deg_nodes_dict.keys() or len(deg_nodes_dict[1]) == 0:
				deg_nodes_dict[1] = set()
				deg_roulette.extend( [1] )
			deg_nodes_dict[1].append(node)
			
			# Shuffle the roulette field.
			random.shuffle(deg_roulette)

			print(g.number_of_nodes(), g.number_of_edges())

except KeyboardInterrupt as e:
	# exit(0)
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
	# print(g.edge[citation[0]][citation[1]]['year'])
	#f.write(str(citation[0])+'\t'+str(citation[1])+'\t'+str(g.edge[citation[0]][citation[1]]['year'])+'\n')
	pass
f.close()
print 'final graph: nodes:',len(g.nodes()),', edges:',len(g.edges())