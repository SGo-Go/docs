#!/usr/bin/python

# import networkx
import os,sympy
try:
    import matplotlib.pyplot as plt
except:
    raise

import networkx as nx
from sympy import Matrix,pprint,init_printing
init_printing(use_latex=True)

def get_stochastic_matrix(G):
    A = nx.adjacency_matrix(G, nodelist=list('ABCDE'))
    k = Matrix((A.sum(axis=0)).astype(int)).applyfunc(lambda x: 1/x)
    A = Matrix(A.astype(int))
    S = A.multiply_elementwise(sympy.ones(5,1)*k)
    return S

edges1 = [('B', 'A'), ('C', 'B'), ('D', 'C'), ('D', 'A'), ('A', 'E'), ('E', 'D')]
edges11 = [('B', 'A'), ('C', 'B'), ('A', 'E'), ('E', 'D')]
edges2 = [('E', 'B'), ('E', 'C')]

def getGraph(edges1, edges2):
    G = nx.DiGraph()
    G.add_edges_from(edges1, weight = 1)
    G.add_edges_from(edges2, weight = 2)
    pos={'A':(0,0),
         'B':(1,0),
         'C':(1,1),
         'D':(0,1),
         'E':(0.5,0.5)}
    return G, pos

def drawGraph(edges1, edges2, labels = None, filename = 'graph.pdf', node_size=1000):
    G,pos = getGraph(edges1, edges2)
    if labels is None: labels = list('ABCDE')

    plt.figure(figsize=(5,5))
    plt.axis('off')
    nx.draw_networkx_nodes(G, pos, nodelist = list('ABCDE'), node_color = 'white', node_size=node_size)
    nx.draw_networkx_edges(G, pos, edgelist=edges1, edge_color='black', width=1, arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=edges2, edge_color='black', width=2, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, dict(zip(edges1+edges2, [1]*len(edges1) + [2]*len(edges2))))
    nx.draw_networkx_labels(G,pos, dict(zip(list('ABCDE'), labels)),font_size=20,color='white')
    plt.savefig("figs/tex/" + filename)

G,pos = getGraph(edges1, edges2)
pprint(get_stochastic_matrix(G))
print sympy.latex(get_stochastic_matrix(G))
M=get_stochastic_matrix(G)

#drawGraph(edges11, edges2, filename = "graph_dead_end.pdf", labels = list('ABCDE'))
#drawGraph(edges1, edges2, filename = "graph.pdf", labels=['']*5, node_size=[100,200,300,400,500])#_probability

drawGraph(edges1, edges2, filename = "graph.pdf", labels = list('ABCDE'))
#v=Matrix([1,0,0,0,0]).T
v_ = ([1,0,0,0,0], [0,0,0,0,1], [0, '2/5','2/5', '1/5', 0])
for i in range(3):
    v=v_[i]
    drawGraph(edges1, edges2, filename = "graph_probability%d.pdf" %i, labels=v)#

#plt.show()
