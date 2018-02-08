#!/usr/bin/env python
import sys

factor=float(sys.argv[1])
for line in open(sys.argv[2]):
	if line.startswith("seqid"): print line.strip()
	else:
		cut=line.strip().split("\t")
		cut[3]=str(float(cut[3])*factor)
		print "\t".join(cut)
		

