#!/usr/bin/python
import json
import argparse as ap
import os, sys
import operator
import sys
import igraph as ig
from collections import defaultdict

get_group = lambda email: 1 if email.endswith("enron.com") else 2

parser = ap.ArgumentParser(description = "Aggregates a list of mail senders "\
        "receivers to plot them in an easier way.")

parser.add_argument("-i", "--in_file", type=ap.FileType("r"),
        default=sys.stdin, help = \
        "The file with pairs of senders and receivers. If not specified, it "\
        "defaults to the standard input.")

parser.add_argument("-t", "--threshold", default=0, type=float, \
        help = "The minimum amount of mails to aggregate. Default is no " \
        "threshold at all.")



args = parser.parse_args()
connections = defaultdict(int)

max_count = 0
with args.in_file as f:
    count = 1
    last_line = f.readline()


    for line in f:
        if line == last_line:
            count += 1
        else:
            if count > max_count:
                max_count = count

            if count >= args.threshold: 
                addresses = last_line.split()
                
                n0 = addresses[0]
                n1 = addresses[1]

                connections[(n0, n1)] = count

            last_line = line
            count = 1



names = sorted(list(set(map(operator.itemgetter(0), connections.keys())) | \
                 set(map(operator.itemgetter(1), connections.keys()))))

node_to_index = { v:k for (k,v) in enumerate(names) }

edges = [ (node_to_index[v[0]], node_to_index[v[1]]) for v in connections.keys()
    ]

weights = [ 1.0/connections[(names[v[0]], names[v[1]])] for v in edges ]

g = ig.Graph(n = len(names), edges = edges, directed = True)
g.es["weights"] = weights

tree = g.spanning_tree(weights=weights, return_tree = True)

ig.plot(g, layout=ig.Graph.layout_reingold_tilford(tree, root)



