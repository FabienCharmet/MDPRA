import sys,re,difflib,time,datetime
import numpy as np
from array import array
np.set_printoptions(threshold=sys.maxsize)
import matplotlib.pyplot as plt
import networkx as nx

def show_graph_with_labels(adjacency_matrix, mylabels):
    rows, cols = np.where(adjacency_matrix != 0)
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.Graph()
    gr.add_edges_from(edges)
    pos=nx.spring_layout(gr)
    nx.draw(gr,pos, node_size=500, with_labels=True, edge_color='b')
    plt.show()

def make_label(labels):
    l = {}
    for i, label in enumerate(labels):
        l[i] = label
    return l


P = np.loadtxt("test2")
show_graph_with_labels(P,make_label(range(len(P)+10)))
