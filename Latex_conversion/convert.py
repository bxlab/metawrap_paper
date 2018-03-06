#!/usr/bin/env python

import sys
for line in open(sys.argv[1]):
	for c in line:
		elif c=="_": sys.stdout.write('\_')
		elif c=="%": sys.stdout.write('\%')
		else: sys.stdout.write(c)
