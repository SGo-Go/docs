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
    A = nx.adjacency_matrix(G.reverse(copy=True), nodelist=list('ABCDE'))
    k = Matrix((A.sum(axis=0)).astype(int)).applyfunc(lambda x: 1/x)
    A = Matrix(A.astype(int))
    S = A.multiply_elementwise(sympy.ones(5,1)*k)
    return S

edges1 = [('B', 'A'), ('C', 'B'), ('D', 'C'), ('D', 'A'), ('A', 'E'), ('E', 'D')]
edges11 = [('C', 'B'), ('D', 'C'), ('D', 'A'), ('A', 'E'), ('E', 'D')]
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
    nx.draw_networkx_labels(G,pos, dict(zip(list('ABCDE'), map(lambda s: '$%s$' % s if s != '' else '', list(labels)))),font_size=20,color='white')
    plt.savefig("figs/tex/" + filename)#, bbox_inches="tight")

G,pos = getGraph(edges1, edges2)
M=get_stochastic_matrix(G)

# pprint(get_stochastic_matrix(G))
# print sympy.latex(get_stochastic_matrix(G))

#drawGraph(edges11, edges2, filename = "graph_dead_end.pdf", labels = list('ABCDE'))
#drawGraph(edges1, edges2, filename = "graphx.pdf", labels=['']*5, node_size=[100,200,300,400,500])#_probability


M=get_stochastic_matrix(G)

# rand surfer
drawGraph(edges1, edges2, filename = "graph.pdf", labels = list('ABCDE'))
v=Matrix([1,0,0,0,0]).T
v_ = ([1,0,0,0,0], [0,0,0,0,1], [0, '\\frac{2}{5}','\\frac{2}{5}', '\\frac{1}{5}', 0])
for i in range(3):
    v= v_[i]
    drawGraph(edges1, edges2, filename = "graph_probability%d.pdf" %i, labels=v)#
    #v = M*v

pr = sympy.ones(len(G.nodes()),1)/len(G.nodes())
node_size=map(int, list(5000*pr))
drawGraph(edges1, edges2, filename = "graph_tansmatr0.pdf", # labels=['']*5, 
          node_size=node_size)
for i in range(1,4):
    prp = M*pr
    # print r"""\only<%i>{{ \begin{{equation*}}
    # {2} = 
    # {0}
    # \cdot
    # {1}
    # \end{{equation*}} }}""".format(*map(sympy.latex, (M, pr, prp))) % i
    # print "\n"*2
    pr = prp
    node_size=map(int, list(5000*pr))
    drawGraph(edges1, edges2, filename = "graph_tansmatr%d.pdf" % i, # labels=['']*5, 
              node_size=node_size)

def get_pageranks(G, alpha=1, nodes = list('ABCDE')):
    pranks = nx.pagerank(G, alpha=alpha)
    return [pranks[k] for k in nodes]
pr = get_pageranks(G)
print map(lambda x: round(100*x)/100., pr)
node_size=map(lambda x : int(5000*x), pr)
drawGraph(edges1, edges2, filename = "graph_tansmatrN.pdf", # labels=['']*5, 
          node_size=node_size)

def drawGraph1(edges1, edges2, edges3, edges4, labels = None, filename = 'graph.pdf', node_size=1000):
    G,pos = getGraph(edges1, edges2)
    if labels is None: labels = list('ABCDE')

    plt.figure(figsize=(5,5))
    plt.axis('off')
    nx.draw_networkx_nodes(G, pos, nodelist = list('ABCDE'), node_color = 'white', node_size=node_size)
    nx.draw_networkx_edges(G, pos, edgelist=edges1, edge_color='black', width=1, arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=edges2, edge_color='black', width=2, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, dict(zip(edges1+edges2, [1]*len(edges1) + [2]*len(edges2))))
    nx.draw_networkx_edges(G, pos, edgelist=edges3, edge_color='gray', style='dashed', width=1, arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=edges4, edge_color='gray', style='dashed', width=2, arrows=True)
    nx.draw_networkx_labels(G,pos, dict(zip(list('ABCDE'), map(lambda s: '$%s$' % s if s != '' else '', list(labels)))),font_size=20,color='white')
    plt.savefig("figs/tex/" + filename)#, bbox_inches="tight")

edges1x = [('D', 'C'), ('D', 'A'), ('A', 'E'), ('E', 'D')]
edges1y = [('C', 'B'), ]
edges2x = [('E', 'C')]
edges2y = [('E', 'B')]
node_size = 1000
drawGraph(edges11, edges2, filename = "graph_dead_end.pdf", node_size=node_size)
drawGraph1(edges1x, edges2x, edges1y, edges2y, filename = "graph_dead_end1.pdf", node_size=node_size)

H = G.copy()
H.remove_node('B')
pr = get_pageranks(H, nodes = list('ACDE'))
print nx.pagerank(H, alpha=1)
print map(lambda x: round(100*x)/100., pr)
node_size=map(lambda x : int(4000*x), pr)
node_size.insert(1, 1000)
print node_size
print "\n"*20
drawGraph1(edges1x, edges2x, edges1y, edges2y, filename = "graph_dead_end2.pdf", node_size=node_size)

node_size[1] = node_size[2] + node_size[4]/5
drawGraph(edges11, edges2, filename = "graph_dead_end3.pdf", node_size=node_size)

Gp = G.copy()
Gp.remove_edge('B','A')
pr = get_pageranks(Gp, alpha = 0.8, nodes = list('ABCDE'))
print map(lambda x: round(100*x)/100., pr)
node_size=map(lambda x : int(5000*x), pr)
print node_size
drawGraph(edges11, edges2, filename = "graph_dead_end_pagerank.pdf", node_size=node_size)

#plt.show()
