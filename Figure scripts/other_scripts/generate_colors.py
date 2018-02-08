#!/usr/bin/env python
import random
import sys


original_string="paultol=list(c("#DDDDDD") ,c("#DDDDDD","#4477AA"), c("#DDDDDD","#4477AA","#CC6677"), c("#DDDDDD","#4477AA","#DDCC77","#CC6677"), c("#DDDDDD","#4477AA","#117733","#DDCC77","#CC6677"), c("#DDDDDD","#332288","#88CCEE","#117733","#DDCC77","#CC6677"), c("#DDDDDD","#332288","#88CCEE","#117733","#DDCC77","#CC6677","#AA4499"), c("#DDDDDD","#332288","#88CCEE","#44AA99","#117733","#DDCC77","#CC6677","#AA4499"), c("#DDDDDD","#332288","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#CC6677","#AA4499"), c("#DDDDDD","#332288","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#CC6677","#882255","#AA4499"), c("#DDDDDD","#332288","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#661100","#CC6677","#882255","#AA4499"), c("#DDDDDD","#332288","#6699CC","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#661100","#CC6677","#882255","#AA4499"), c("#DDDDDD","#332288","#6699CC","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#661100","#CC6677","#AA4466","#882255","#AA4499"), c("#DDDDDD","#332288","#6699CC","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#661100","#CC6677","#AA4466","#882255","#AA4499","#777777"))"


color_list=["#DDDDDD"]
print color_list
for i in range(1000):
	r = lambda: random.randint(0,255)
	c=('#%02X%02X%02X' % (r(),r(),r()))
	color_list.append(c)


sys.stdout.write("colors=list(")
for c in color_list:
	sys.stdout.write('"')
	sys.stdout.write(c)
	sys.stdout.write('", ')
	
sys.stdout.write('"#777777")')

