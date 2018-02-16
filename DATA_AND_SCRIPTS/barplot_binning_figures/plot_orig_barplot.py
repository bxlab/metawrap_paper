#!/usr/bin/env python
import sys
import numpy as np
import matplotlib.pyplot as plt



samples=["Water", "Gut", "Soil"]
# load in data
data={}
for sample in samples:
	data[sample]={}
	categories=[]
	for line in open(sample+".tab"):
		cut=line.strip().split("\t")
		if cut[0]=="Completion":
			binners=cut[1:]
		else:
			for i in range(1, len(cut)):
				cut[i]=int(cut[i])
			data[sample][cut[0]]=cut[1:]
			categories.append(cut[0])

# plot basics
fig = plt.figure(figsize=(12,8))
colors=["#000033", "#000099", "#0000ff", "#6666ff"]
width = 0.85

# make barplots
n=0
for sample in samples:
	print sample
	n+=1
	ax = fig.add_subplot(310+n)
	
	# guide tick marks
	if sample=="Water": inc=25
	if sample=="Gut": inc=20
	if sample=="Soil": inc=10
	for y in range(0, 300, inc):
		plt.plot(range(-1, 14), [y] * len(range(-1, 14)), "--", lw=0.2, color="black", alpha=0.3, dashes=(15, 15))

	# set y boundaries
	if sample=="Water": plt.ylim(0, 210)
	if sample=="Gut": plt.ylim(0, 150)
	if sample=="Soil": plt.ylim(0, 55)
	plt.xlim(-1, 13)



	prev=None
	patch_handles=[]
	patch_handle_labels=[]
	N=len(binners); ind = np.arange(N)
	for i, category in enumerate(categories):
		bars=data[sample][category][:]
		patch_handles.append(ax.bar(ind, bars, width, bottom=prev, label=category, color=colors[i]))
		if prev==None: 
			prev=bars[:]
			labels=bars[:]
		else:
			for i, val in enumerate(bars):
				labels[i]-=val
				val=prev[i]+val
				prev[i]=val
		patch_handle_labels.append(bars)

	# add labels
	cumulative_height=[]
	for i in range(len(patch_handles[0])): cumulative_height.append(0)
	for j in range(len(patch_handles)):
		for i, patch in enumerate(patch_handles[j].get_children()):
			bl = patch.get_xy()
			x = 0.5*patch.get_width() + bl[0]
			y = patch.get_height()/3 + cumulative_height[i]
			cumulative_height[i]+=patch_handle_labels[j][i]
			ax.text(x,y, str(patch_handle_labels[j][i]), ha='center', color='w')

	# remove borders
	ax.spines["top"].set_visible(False)
	ax.spines["bottom"].set_linewidth(0.5)
	ax.spines['bottom'].set_color('black')
	ax.spines["right"].set_visible(False)
	ax.spines["left"].set_visible(False)

	
	ax.set_facecolor('white')
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	plt.ylabel(sample+' Bins', fontsize=16)

	#rename binners:
	binners[3]="Binning_ref."
	binners[9:13]=["mW.R>70", "mW.R>80", "mW.R>90", "mW.R>95"]
	binners[5:9]=["mW>70", "mW>80", "mW>90", "mW>95"]
	
	plt.yticks(fontsize=14)
	for tick in ax.get_xticklabels():
		tick.set_rotation(45)
	if n==1: plt.title('Binning performance comparison', fontsize=30)
	if n==3: 
		plt.xticks(ind, binners, ha='right', fontsize=14)
		legend=plt.legend(bbox_to_anchor=(0.9, -0.4), ncol=4, facecolor=None, prop={'size': 16}, frameon=False, title=None, columnspacing=0.5)
		
		#ax.text(5, -25, 'metaWRAP', fontsize=14)
		#ax.text(8, -25, 'metaWRAP reassembled', fontsize=14)

	else: plt.xticks([], [])
	#plt.yticks(np.arange(0, 81, 10))
	
plt.tight_layout(h_pad=0)
plt.subplots_adjust(top=0.95, right=0.95, left=0.15, bottom=0.2)
plt.savefig(sys.argv[1],format='eps', dpi=600)
plt.show()





