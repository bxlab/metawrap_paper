#!/usr/bin/env python
# USAGE:
# ./script file1.stats file2.stats file3.stats

import sys
import matplotlib.pyplot as plt
plt.switch_backend('agg')

min_completion=50
min_precision=90
####################################################################################################################################
############################################         CAMI_low COMPLETION PLOT           ############################################
####################################################################################################################################
print "Loading completion info...."
data={}
max_x=0
# loop over all bin .stats files
for file_name in sys.argv[1:]:
	bin_set=".".join(file_name.split("/")[-1].split(".")[:-1])
	data[bin_set]=[]
	for line in open("CAMI_low/"+file_name):
		# skip header
		if "precision" in line: continue
		# skip bins that are too contaminated or very incomplete
		if line.split("\t")[1]=="NA": continue
		if float(line.split("\t")[1])<1.0*min_precision/100: continue
		if float(line.split("\t")[2])<1.0*min_completion/100: continue
		# save the completion value of each bin into a list
		data[bin_set].append(100*float(line.split("\t")[2]))

	
	if len(data[bin_set])>max_x: max_x=len(data[bin_set])

# sort the completion data sets
for bin_set in data:
	data[bin_set].sort(reverse=True)

print "Plotting completion data..."
# MAKING THE PLOT PRETTY!!!!
# set some color schemes
tableau20 = [(214, 39, 40), (31, 119, 180), (255, 127, 14),    
             (44, 160, 44), (255, 15, 150),    
             (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

for i in range(len(tableau20)):    
	r, g, b = tableau20[i]    
	tableau20[i] = (r / 255., g / 255., b / 255.)
plot_colors={}
for i, label in enumerate(sys.argv[1:]):
	bin_set=".".join(label.split("/")[-1].split(".")[:-1])
	plot_colors[bin_set]=tableau20[i]



# set figure size
plt.figure(figsize=(16, 12))
plt.style.use('ggplot')

# Remove the plot frame lines. They are unnecessary chartjunk.    
ax = plt.subplot(321)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_linewidth(0.5)
ax.spines['bottom'].set_color('black')
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.set_facecolor('white')

# Ensure that the axis ticks only show up on the bottom and left of the plot.    
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# Limit the range of the plot to only where the data is.    
plt.ylim(min_completion, 105)
max_x=0
for k in data:
	if len(data[k])>max_x: max_x=len(data[k])
plt.xlim(0, max_x)

# Make sure your axis ticks are large enough to be easily read.    
plt.yticks(range(min_completion, 105, 10), [str(float(x)/100) for x in range(min_completion, 105, 10)], fontsize=14)    
plt.xticks(fontsize=14)    

# Provide tick lines across the plot to help your viewers trace along    
for y in range(min_completion, 105, 10):    
	plt.plot(range(0, max_x), [y] * len(range(0, max_x)), "--", lw=0.2, color="black", alpha=0.3, dashes=(15, 15))
  
# Remove the tick marks; they are unnecessary with the tick lines we just plotted.    
plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")    


# PLOTTING THE DATA

# prepare labeles
labels = []
for k in data: labels.append(k)

# make ranking system for lable distribution
ranks={}
for bin_set in labels:
	p=len(data[bin_set])
	ranks[bin_set]=p
rank_order={}
n=0
for key, value in sorted(ranks.iteritems(), key=lambda (k,v): (v,k), reverse=True):
	rank_order[key]=n
	n+=1

# start plotting data
for rank, bin_set in enumerate(labels):
	# chose a color!
	c=plot_colors[bin_set]

	# plot the data
	if bin_set=="MaxBin2" or bin_set=="metaBAT2" or bin_set=="CONCOCT": plt.plot(data[bin_set], lw=2.5, color=c, linestyle='dashed')
	else: plt.plot(data[bin_set], lw=2.5, color=c)
	
	# add bin set label to plot
	x_pos=len(data[bin_set])-1# - (len(rank_order)-rank_order[bin_set]-1)*10 -1
	if "DAS" in bin_set: x_pos-=1
	if "WRAP" in bin_set: x_pos-=0
	if "refiner" in bin_set: x_pos-=3
	y_pos = data[bin_set][x_pos]
	if "CONCO" in bin_set: y_pos-=2
	if "WRAP" in bin_set: y_pos-=5
	plt.text(x_pos, y_pos, bin_set, fontsize=18, color=c)

# add plot and axis titles and adjust edges
plt.title("Bin recall", fontsize=36) 
plt.ylabel("Bin recall", fontsize=20)

plt.text(-0.25*max_x, 75, "CAMI_low", fontsize=30, ha="center", rotation='vertical', verticalalignment='center')



####################################################################################################################################
############################################         CAMI_low CONTAMINATION PLOT        ############################################
####################################################################################################################################
print "Loading contamination info..."

data={}
# loop over all bin .stats files
for file_name in sys.argv[1:]:
	bin_set=".".join(file_name.split("/")[-1].split(".")[:-1])
	data[bin_set]=[]
	for line in open("CAMI_low/"+file_name):
		# skip header
		if "precision" in line: continue

		# skip bins that are too incomplete or way too contaminated
		if line.split("\t")[1]=="NA": continue
		if float(line.split("\t")[2])<1.0*min_completion/100: continue
		if float(line.split("\t")[1])<1.0*min_precision/100: continue
		if float(line.split("\t")[1])==0: continue
		# save the contamination value of each bin into a list
		data[bin_set].append(100*float(line.split("\t")[1]))

# sort the contamination data sets
for bin_set in data:
	data[bin_set].sort(reverse=True)

print "Plotting the contamination data..."
# MAKING THE PLOT PRETTY!!!!
# Remove the plot frame lines. They are unnecessary chartjunk.    
ax = plt.subplot(322)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_linewidth(0.5)
ax.spines['bottom'].set_color('black')
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.set_facecolor('white')

# Ensure that the axis ticks only show up on the bottom and left of the plot.    
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# Limit the range of the plot to only where the data is.    
#plt.gca().invert_yaxis()
plt.ylim(min_precision, 101)
#ax.set_yscale('log')
max_x=0
for k in data:
	if len(data[k])>max_x: max_x=len(data[k])
plt.xlim(0, max_x)

# Make sure your axis ticks are large enough to be easily read.    
plt.yticks(range(min_precision, 102, 2), [str(float(x)/100) for x in range(min_precision, 102, 2)], fontsize=14)
plt.xticks(fontsize=14)    

# Provide tick lines across the plot to help your viewers trace along    
for y in range(min_precision, 102, 2):
	plt.plot(range(0, max_x), [y] * len(range(0, max_x)), "--", lw=0.2, color="black", alpha=0.3, dashes=(15, 15))    
  
# Remove the tick marks; they are unnecessary with the tick lines we just plotted.    
plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")    


# PLOTTING THE DATA
# prepare labeles
labels = []
for k in data: labels.append(k)


# start plotting data
for rank, bin_set in enumerate(labels):
	# chose a color!
	c=plot_colors[bin_set]

	# plot the data
        if bin_set=="MaxBin2" or bin_set=="metaBAT2" or bin_set=="CONCOCT": plt.plot(data[bin_set], lw=2.5, color=c, linestyle='dashed')
        else: plt.plot(data[bin_set], lw=2.5, color=c)
	
	# add plot label
	#x_pos = len(data[bin_set])-1-20*(len(rank_order)-rank_order[bin_set]-1)
	x_pos = len(data[bin_set])-1#*95/100
	if "DAS" in bin_set: x_pos-=5
	if "WRAP" in bin_set: x_pos-=0
	if "BAT" in bin_set:x_pos-=1
	y_pos = data[bin_set][x_pos]
	if "WRAP" in bin_set: y_pos-=0.5
	plt.text(x_pos, y_pos, bin_set, fontsize=18, color=c)

# add plot and axis titles and adjust the edges
plt.title("Bin precision", fontsize=36) 
plt.ylabel("Bin precision", fontsize=20)
plt.gcf().subplots_adjust(right=0.9)


####################################################################################################################################
############################################         CAMI_medium COMPLETION PLOT           ############################################
####################################################################################################################################
print "Loading completion info...."
data={}
max_x=0
# loop over all bin .stats files
for file_name in sys.argv[1:]:
	bin_set=".".join(file_name.split("/")[-1].split(".")[:-1])
	data[bin_set]=[]
	for line in open("CAMI_medium/"+file_name):
		# skip header
		if "precision" in line: continue
		# skip bins that are too contaminated or very incomplete
		if line.split("\t")[1]=="NA": continue
		if float(line.split("\t")[1])<1.0*min_precision/100: continue
		if float(line.split("\t")[2])<1.0*min_completion/100: continue
		# save the completion value of each bin into a list
		data[bin_set].append(100*float(line.split("\t")[2]))


	if len(data[bin_set])>max_x: max_x=len(data[bin_set])

# sort the completion data sets
for bin_set in data:
	data[bin_set].sort(reverse=True)

print "Plotting completion data..."


# Remove the plot frame lines. They are unnecessary chartjunk.
ax = plt.subplot(323)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_linewidth(0.5)
ax.spines['bottom'].set_color('black')
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.set_facecolor('white')

# Ensure that the axis ticks only show up on the bottom and left of the plot.
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# Limit the range of the plot to only where the data is.
plt.ylim(min_completion, 105)
max_x=0
for k in data:
	if len(data[k])>max_x: max_x=len(data[k])
plt.xlim(0, max_x)

# Make sure your axis ticks are large enough to be easily read.
plt.yticks(range(min_completion, 105, 10), [str(float(x)/100) for x in range(min_completion, 105, 10)], fontsize=14)
plt.xticks(fontsize=14)

# Provide tick lines across the plot to help your viewers trace along
for y in range(min_completion, 105, 10):
	plt.plot(range(0, max_x), [y] * len(range(0, max_x)), "--", lw=0.2, color="black", alpha=0.3, dashes=(15, 15))

# Remove the tick marks; they are unnecessary with the tick lines we just plotted.
plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")


# PLOTTING THE DATA

# prepare labeles
labels = []
for k in data: labels.append(k)

# make ranking system for lable distribution
ranks={}
for bin_set in labels:
	p=len(data[bin_set])
	ranks[bin_set]=p
rank_order={}
n=0
for key, value in sorted(ranks.iteritems(), key=lambda (k,v): (v,k), reverse=True):
	rank_order[key]=n
	n+=1

# start plotting data
for rank, bin_set in enumerate(labels):
	# chose a color!
	c=plot_colors[bin_set]

	# plot the data
        if bin_set=="MaxBin2" or bin_set=="metaBAT2" or bin_set=="CONCOCT": plt.plot(data[bin_set], lw=2.5, color=c, linestyle='dashed')
        else: plt.plot(data[bin_set], lw=2.5, color=c)


	# add bin set label to plot
	x_pos=len(data[bin_set])-1# - (len(rank_order)-rank_order[bin_set]-1)*10 -1
	if "DAS" in bin_set: x_pos-=0
	if "WRAP" in bin_set: x_pos-=2
	if "Max" in bin_set: x_pos-=2
	if "refiner" in bin_set: x_pos-=10
	y_pos = data[bin_set][x_pos]
	if "Max" in bin_set: y_pos-=5
	plt.text(x_pos, y_pos, bin_set, fontsize=18, color=c)

# add plot and axis titles and adjust edges
plt.ylabel("Bin recall", fontsize=20)
plt.text(-0.25*max_x, 75, "CAMI_medium", fontsize=30, ha="center", rotation='vertical', verticalalignment='center')



####################################################################################################################################
############################################         CAMI_medium CONTAMINATION PLOT        ############################################
####################################################################################################################################
print "Loading contamination info..."

data={}
# loop over all bin .stats files
for file_name in sys.argv[1:]:
	bin_set=".".join(file_name.split("/")[-1].split(".")[:-1])
	data[bin_set]=[]
	for line in open("CAMI_medium/"+file_name):
		# skip header
		if "precision" in line: continue

		# skip bins that are too incomplete or way too contaminated
		if line.split("\t")[1]=="NA": continue
		if float(line.split("\t")[2])<1.0*min_completion/100: continue
		if float(line.split("\t")[1])<1.0*min_precision/100: continue
		if float(line.split("\t")[1])==0: continue
		# save the contamination value of each bin into a list
		data[bin_set].append(100*float(line.split("\t")[1]))

# sort the contamination data sets
for bin_set in data:
	data[bin_set].sort(reverse=True)

print "Plotting the contamination data..."
# MAKING THE PLOT PRETTY!!!!
# Remove the plot frame lines. They are unnecessary chartjunk.
ax = plt.subplot(324)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_linewidth(0.5)
ax.spines['bottom'].set_color('black')
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.set_facecolor('white')

# Ensure that the axis ticks only show up on the bottom and left of the plot.
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# Limit the range of the plot to only where the data is.
#plt.gca().invert_yaxis()
plt.ylim(min_precision, 101)
#ax.set_yscale('log')
max_x=0
for k in data:
	if len(data[k])>max_x: max_x=len(data[k])
plt.xlim(0, max_x)

# Make sure your axis ticks are large enough to be easily read.
plt.yticks(range(min_precision, 102, 2), [str(float(x)/100) for x in range(min_precision, 102, 2)], fontsize=14)
plt.xticks(fontsize=14)

# Provide tick lines across the plot to help your viewers trace along
for y in range(min_precision, 102, 2):
	plt.plot(range(0, max_x), [y] * len(range(0, max_x)), "--", lw=0.2, color="black", alpha=0.3, dashes=(15, 15))

# Remove the tick marks; they are unnecessary with the tick lines we just plotted.
plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")


# PLOTTING THE DATA
# prepare labeles
labels = []
for k in data: labels.append(k)


# start plotting data
for rank, bin_set in enumerate(labels):
	# chose a color!
	c=plot_colors[bin_set]

	# plot the data
        if bin_set=="MaxBin2" or bin_set=="metaBAT2" or bin_set=="CONCOCT": plt.plot(data[bin_set], lw=2.5, color=c, linestyle='dashed')
        else: plt.plot(data[bin_set], lw=2.5, color=c)


	# add plot label
	#x_pos = len(data[bin_set])-1-20*(len(rank_order)-rank_order[bin_set]-1)
	x_pos = len(data[bin_set])-1#*95/100
	if "DAS" in bin_set: x_pos-=5
	if "WRAP" in bin_set: x_pos-=3
	y_pos = data[bin_set][x_pos]
	plt.text(x_pos, y_pos, bin_set, fontsize=18, color=c)

# add plot and axis titles and adjust the edges
plt.ylabel("Bin precision", fontsize=20)
plt.gcf().subplots_adjust(right=0.9)


####################################################################################################################################
############################################         CAMI_high COMPLETION PLOT           ############################################
####################################################################################################################################
print "Loading completion info...."
data={}
max_x=0
# loop over all bin .stats files
for file_name in sys.argv[1:]:
	bin_set=".".join(file_name.split("/")[-1].split(".")[:-1])
	data[bin_set]=[]
	for line in open("CAMI_high/"+file_name):
		# skip header
		if "precision" in line: continue
		# skip bins that are too contaminated or very incomplete
		if line.split("\t")[1]=="NA": continue
		if float(line.split("\t")[1])<1.0*min_precision/100: continue
		if float(line.split("\t")[2])<1.0*min_completion/100: continue
		# save the completion value of each bin into a list
		data[bin_set].append(100*float(line.split("\t")[2]))


	if len(data[bin_set])>max_x: max_x=len(data[bin_set])

# sort the completion data sets
for bin_set in data:
	data[bin_set].sort(reverse=True)

print "Plotting completion data..."
# MAKING THE PLOT PRETTY!!!!

# Remove the plot frame lines. They are unnecessary chartjunk.
ax = plt.subplot(325)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_linewidth(0.5)
ax.spines['bottom'].set_color('black')
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.set_facecolor('white')

# Ensure that the axis ticks only show up on the bottom and left of the plot.
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# Limit the range of the plot to only where the data is.
plt.ylim(min_completion, 105)
max_x=0
for k in data:
	if len(data[k])>max_x: max_x=len(data[k])
plt.xlim(0, max_x)

# Make sure your axis ticks are large enough to be easily read.
plt.yticks(range(min_completion, 105, 10), [str(float(x)/100) for x in range(min_completion, 105, 10)], fontsize=14)
plt.xticks(fontsize=14)

# Provide tick lines across the plot to help your viewers trace along
for y in range(min_completion, 105, 10):
	plt.plot(range(0, max_x), [y] * len(range(0, max_x)), "--", lw=0.2, color="black", alpha=0.3, dashes=(15, 15))

# Remove the tick marks; they are unnecessary with the tick lines we just plotted.
plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")


# PLOTTING THE DATA

# prepare labeles
labels = []
for k in data: labels.append(k)

# make ranking system for lable distribution
ranks={}
for bin_set in labels:
	p=len(data[bin_set])
	ranks[bin_set]=p
rank_order={}
n=0
for key, value in sorted(ranks.iteritems(), key=lambda (k,v): (v,k), reverse=True):
	rank_order[key]=n
	n+=1

# start plotting data
for rank, bin_set in enumerate(labels):
	# chose a color!
	c=plot_colors[bin_set]

	# plot the data
        if bin_set=="MaxBin2" or bin_set=="metaBAT2" or bin_set=="CONCOCT": plt.plot(data[bin_set], lw=2.5, color=c, linestyle='dashed')
        else: plt.plot(data[bin_set], lw=2.5, color=c)


	# add bin set label to plot
	x_pos=len(data[bin_set])-1# - (len(rank_order)-rank_order[bin_set]-1)*10 -1
	if "DAS" in bin_set: x_pos-=0
	if "WRAP" in bin_set: x_pos-=0
	if "refiner" in bin_set: x_pos-=5
	if "BAT" in bin_set: x_pos-=20
	y_pos = data[bin_set][x_pos]
	plt.text(x_pos, y_pos, bin_set, fontsize=18, color=c)

# add plot and axis titles and adjust edges
plt.xlabel("Bin recall ranking", fontsize=20)
plt.ylabel("Bin recall", fontsize=20)
plt.text(-0.25*max_x, 75, "CAMI_high", fontsize=30, ha="center", rotation='vertical', verticalalignment='center')



####################################################################################################################################
############################################         CAMI_high CONTAMINATION PLOT        ############################################
####################################################################################################################################
print "Loading contamination info..."

data={}
# loop over all bin .stats files
for file_name in sys.argv[1:]:
	bin_set=".".join(file_name.split("/")[-1].split(".")[:-1])
	data[bin_set]=[]
	for line in open("CAMI_high/"+file_name):
		# skip header
		if "precision" in line: continue

		# skip bins that are too incomplete or way too contaminated
		if line.split("\t")[1]=="NA": continue
		if float(line.split("\t")[2])<1.0*min_completion/100: continue
		if float(line.split("\t")[1])<1.0*min_precision/100: continue
		if float(line.split("\t")[1])==0: continue
		# save the contamination value of each bin into a list
		data[bin_set].append(100*float(line.split("\t")[1]))

# sort the contamination data sets
for bin_set in data:
	data[bin_set].sort(reverse=True)

print "Plotting the contamination data..."
# MAKING THE PLOT PRETTY!!!!
# Remove the plot frame lines. They are unnecessary chartjunk.
ax = plt.subplot(326)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_linewidth(0.5)
ax.spines['bottom'].set_color('black')
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.set_facecolor('white')

# Ensure that the axis ticks only show up on the bottom and left of the plot.
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# Limit the range of the plot to only where the data is.
#plt.gca().invert_yaxis()
plt.ylim(min_precision, 101)
#ax.set_yscale('log')
max_x=0
for k in data:
	if len(data[k])>max_x: max_x=len(data[k])
plt.xlim(0, max_x)

# Make sure your axis ticks are large enough to be easily read.
plt.yticks(range(min_precision, 102, 2), [str(float(x)/100) for x in range(min_precision, 102, 2)], fontsize=14)
plt.xticks(fontsize=14)

# Provide tick lines across the plot to help your viewers trace along
for y in range(min_precision, 102, 2):
	plt.plot(range(0, max_x), [y] * len(range(0, max_x)), "--", lw=0.2, color="black", alpha=0.3, dashes=(15, 15))

# Remove the tick marks; they are unnecessary with the tick lines we just plotted.
plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")


# PLOTTING THE DATA
# prepare labeles
labels = []
for k in data: labels.append(k)


# start plotting data
for rank, bin_set in enumerate(labels):
	# chose a color!
	c=plot_colors[bin_set]

	# plot the data
        if bin_set=="MaxBin2" or bin_set=="metaBAT2" or bin_set=="CONCOCT": plt.plot(data[bin_set], lw=2.5, color=c, linestyle='dashed')
        else: plt.plot(data[bin_set], lw=2.5, color=c)



	# add plot label
	#x_pos = len(data[bin_set])-1-20*(len(rank_order)-rank_order[bin_set]-1)
	x_pos = len(data[bin_set])-1#*95/100
	if "DAS" in bin_set: x_pos-=6
	if "WRAP" in bin_set: x_pos-=5
	if "Max" in bin_set: x_pos-=1
	y_pos = data[bin_set][x_pos]
	plt.text(x_pos, y_pos, bin_set, fontsize=18, color=c)

# add plot and axis titles and adjust the edges
plt.xlabel("Bin precision ranking", fontsize=20)
plt.ylabel("Bin precision", fontsize=20)
plt.gcf().subplots_adjust(right=0.9)
















# save figure
print "Saving figures binning_results.eps and binning_results.png ..."
plt.tight_layout(w_pad=20)
plt.subplots_adjust(top=0.95, right=0.85, left=0.10, bottom=0.06)
plt.savefig("binning_results.eps",format='eps', dpi=600)
#plt.savefig("binning_results.png",format='png', dpi=600)
#plt.show()






