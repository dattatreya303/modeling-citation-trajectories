import networkx as nx
import numpy as np
from scipy.stats import pareto
import itertools
import math
from numpy.linalg import norm
import sys
import random
from matplotlib import pyplot as plt
import json

pareto_r = lambda s: np.random.pareto(1,s)
paretoCDF_x = lambda x: pareto.cdf(x,1)

t = 0

start_year = 1960
end_year = 1975
file_name = 'newData_initial_graph_'+str(start_year)+'_'+str(end_year)
g = nx.read_adjlist('./'+file_name, create_using=nx.DiGraph())
print 'initial graph: nodes:',len(g.nodes()),', edges:',len(g.edges())

for citation in g.edges():
	g.edge[citation[0]][citation[1]]['year'] = t

alpha = -3
K_not = 0.1
N = g.number_of_nodes()
C = float(alpha+1) / (math.pow(N,alpha+1)-math.pow(K_not,alpha+1))

for paper in g.nodes():
	fit = pareto_r(1)
	g.node[paper]['fitness'] = fit
	g.node[paper]['link_p'] = math.exp( paretoCDF_x(fit) / float(C) )
	
try:
		
		node_edges_dict = dict()
		with open('node_edges_dict') as f:
			node_edges_dict = json.load(f)

		node_year_dict = dict()
		with open('node_year_dict') as f:
			node_year_dict = json.load(f)

		nodes_by_year = sorted(node_year_dict.keys(), key = lambda x: int(node_year_dict[str(x)]) )
		
		deg_nodes_dict = dict()
		for node in g.nodes():
			deg = g.in_degree(node)
			if deg not in deg_nodes_dict.keys():
				deg_nodes_dict[deg] = set()
			deg_nodes_dict[deg].add( node )

		i = 0
		newEdges = []
		curYear = end_year
		for node in nodes_by_year:

			i += 1
			print(i)

			if int(node_year_dict[node]) <= end_year:
				continue
			
			if int(node_year_dict[node]) > 1995:
				#break
				pass
			
			if int(node_year_dict[node]) != curYear:
				t = t + ( int(node_year_dict[node]) - curYear)
				print("********* {0} *********".format(t))
				curYear = int(node_year_dict[node])

			K_not = 0.1
			N = g.number_of_nodes()
			C = float(alpha+1) / (math.pow(N,alpha+1)-math.pow(K_not,alpha+1))
			G_coef = math.sqrt( K_not / ( N * C * (math.exp(1/float(C))-1) ) )
			
			fit = pareto_r(1)
			g.add_node( node, fitness=fit, link_p=math.exp(paretoCDF_x(fit) / float(C)) )
			
			link_probs = [ (math.pow(G_coef,2)*g.node[p]['link_p']*g.node[node]['link_p'], p) for p in g.nodes() ]
			link_probs.sort()
			
			k = 1
			if node in node_edges_dict.keys():
				k = 1 + len(node_edges_dict[node])

			newEdges[:] = []
			for j in range(k):
				tp = sum([p[0] for p in link_probs])
				rv = np.random.uniform(tp)
				s = 0
				for pl in link_probs:
					s += pl[0]
					if s >= rv:
						link_probs = [ pl1 for pl1 in link_probs if pl1[1] != pl[1] ]
						newEdges.append(pl[1])
						break
			
			for e in newEdges:
				g.add_edge(node, e)
				g.edge[node][e]['year'] = t

			print(g.number_of_nodes(), g.number_of_edges())

except KeyboardInterrupt as e:
	pass


# saving network in the form of an edge list
out_papers = './final_results1/AllPapersSim_fromNew'
out_edges = './final_results1/TemporalEdgeListSim_fromNew'
f = open(out_papers, 'wb')
for paper in g.nodes():
	f.write(str(paper)+'\n')
f.close()
f = open(out_edges, 'wb')
for citation in g.edges():
	f.write(str(citation[0])+'\t'+str(citation[1])+'\t'+str(g.edge[citation[0]][citation[1]]['year'])+'\n')
f.close()
print 'final graph: nodes:',len(g.nodes()),', edges:',len(g.edges())