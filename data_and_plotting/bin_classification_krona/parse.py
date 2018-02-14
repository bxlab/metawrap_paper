#!/usr/bin/env python
import sys
for line in open(sys.argv[1]):
	t=line.strip().split("\t")[1].split(";")
	for i in range(len(t)): t[i]="_".join(t[i].split("_")[:-1])
	print "\t".join(t)
	
