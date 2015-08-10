#!/usr/bin/python
import json
import argparse as ap
import os, sys
import operator
import sys
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

parser.add_argument("-p", "--pretty", action="store_true", help = "Pretty print the "  \
        "output file.")

parser.add_argument("-o", "--out_file", type=ap.FileType("w"), default=sys.stdout, help = \
    "The file to be output. If not specified, the standard output will be used.")

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

names_indexes = { v: k for k, v in enumerate(names) }

nodes = [ { \
          "name": names[i], \
          "index": i, \
          "group": get_group(names[i]), \
          "color_value": 0, \
          "size": 20 } \
          for i in range(len(names)) ]


links = [ { \
          "source": names_indexes[k[0]], \
          "target": names_indexes[k[1]], \
          "value": v } \
          for k, v in connections.iteritems() ]

print [v for k, v in connections.iteritems() ]
exit()
with args.out_file as out_file:

        if args.pretty:
            out_file.write(json.dumps( {\
                "max_count": max_count, \
                "nodes" : nodes, \
                "links" : links }, \
                indent = 4, separators = (",",":")))
        else:
            out_file.write(json.dumps( { \
                "max_count": max_count, \
                "nodes" : nodes, \
                "links" : links } ))



