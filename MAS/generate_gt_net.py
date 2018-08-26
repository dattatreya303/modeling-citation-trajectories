import networkx as nx
import numpy as np
import itertools
from math import exp
from numpy.linalg import norm
import sys
import random
from matplotlib import pyplot as plt
import json
from collections import Counter

# Creating a node:[edges] dictionary.
node_edges_dict = dict()
with open('node_edges_dict') as f:
	node_edges_dict = json.load(f)

# Creating a node:year dictionary..
node_year_dict = dict()
with open('node_year_dict') as f:
	node_year_dict = json.load(f)

t = 0	# time counter

# loading initial graph generated from real data
file_name = 'newData_initial_graph'
g = nx.read_adjlist('./'+file_name, create_using=nx.DiGraph())
print 'initial graph: nodes:',len(g.nodes()),', edges:',len(g.edges())

# initializing year attributes for each citation
c = []
for citation in g.edges():
	g.edge[citation[0]][citation[1]]['year'] = min(1975,int(node_year_dict[citation[0]]) - 1960)
t = 15

try:
		# Sorting nodes according to the year in which they appeared.
		nodes_by_year = sorted(node_year_dict.keys(), key = lambda x: int(node_year_dict[str(x)]) )
		
		# for i in range(10):
		# 	print(nodes_by_year[i], node_year_dict[nodes_by_year[i]])

		i = 0
		newEdges = []
		curYear = end_year
		ne = 0
		for newNode in nodes_by_year:

			# print("...... {0} ......".format(len(deg_roulette)))

			i += 1
			#print(i)

			if int(node_year_dict[newNode]) <= end_year:
				continue
			
			if int(node_year_dict[newNode]) > 2010:
				break
			
			# Changing year.
			if int(node_year_dict[newNode]) != curYear:
				t = t + ( int(node_year_dict[newNode]) - curYear)
				print("********* {0} *********".format(t))
				curYear = int(node_year_dict[newNode])
			
			if newNode in node_edges_dict:
				newEdges = [ e for e in node_edges_dict[newNode] ]	
			g.add_node( newNode )

			for e in newEdges:
				g.add_edge(newNode, e)
				g.edge[newNode][e]['year'] = t
				#if e not in g.nodes():
				#	ne += 1
				# exit(0)
			
			#print(g.number_of_nodes(), g.number_of_edges())

except KeyboardInterrupt as e:
	# exit(0)
	pass


# saving network in the form of an edge list
out_papers = './AllPapersSim_MAS60_75_2010'
out_edges = './TemporalEdgeListSim_MAS60_75_2010'
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
