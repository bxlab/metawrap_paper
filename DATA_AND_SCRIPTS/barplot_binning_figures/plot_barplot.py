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
			cut=cut[:6]+[" "]+cut[6:10]+[" "]+cut[10:]
			binners=cut[1:]
		else:
			for i in range(1, len(cut)):
				cut[i]=int(cut[i])
			cut=cut[:6]+[0]+cut[6:10]+[0]+cut[10:]
			data[sample][cut[0]]=cut[1:]
			categories.append(cut[0])

# plot basics
fig = plt.figure(figsize=(12,6))
colors=["#000033", "#000099", "#0000ff", "#6666ff"]
width = 0.85

# make barplots
n=0
for sample in samples:
	print sample
	n+=1
	ax = fig.add_subplot(130+n)
	
	# guide tick marks
	if sample=="Water": inc=50
	if sample=="Gut": inc=25
	if sample=="Soil": inc=10
	for x in range(0, 300, inc):
		plt.plot([x] * len(range(-1, len(binners)+1)), range(-1, len(binners)+1), "--", lw=0.2, color="black", alpha=0.35, dashes=(15, 15))

	# set y boundaries
	if sample=="Water": plt.xlim(0, 201)
	if sample=="Gut": plt.xlim(0, 151)
	if sample=="Soil": plt.xlim(0, 51)
	plt.ylim(-1, len(binners))



	prev=None
	patch_handles=[]
	patch_handle_labels=[]
	N=len(binners); ind = np.arange(N)[::-1]
	for i, category in enumerate(categories):
		bars=data[sample][category][:]
		patch_handles.append(ax.barh(ind, bars, width, left=prev, label=category, color=colors[i], edgecolor = "w"))
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
	cumulative_width=[]
	for i in range(len(patch_handles[0])): cumulative_width.append(0)
	for j in range(len(patch_handles)):
		for i, patch in enumerate(patch_handles[j].get_children()):
			bl = patch.get_xy()
			y = 0.22*patch.get_height() + bl[1] 
			x = patch.get_width()/2 + cumulative_width[i]
			cumulative_width[i]+=patch_handle_labels[j][i]
			if patch_handle_labels[j][i]!=0: ax.text(x,y, str(patch_handle_labels[j][i]), ha='center', color='w', fontsize=12)

	# remove borders
	ax.spines["top"].set_visible(False)
	ax.spines["bottom"].set_linewidth(0.5)
	ax.spines['bottom'].set_color('black')
	ax.spines["right"].set_visible(False)
	ax.spines["left"].set_visible(False)

	
	ax.set_facecolor('white')
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")

	#rename binners:
	binners[3]="Binning_ref."
	binners[6:10]=["-c 70", "-c 80", "-c 90", "-c 95"]
	binners[11:15]=["-c 70", "-c 80", "-c 90", "-c 95"]
	
	plt.yticks(fontsize=14)
	plt.xticks(fontsize=14)
	for tick in ax.get_xticklabels():
		tick.set_rotation(0)
	plt.title(sample+" Bins", fontsize=20) 
	if n==1: 
		plt.yticks(ind, binners, ha='right', fontsize=14)
		legend=plt.legend(bbox_to_anchor=(2.5, -0.08), ncol=4, facecolor=None, prop={'size': 16}, frameon=False, title=None, columnspacing=0.8)
		ax.text(-75,6.5, "MetaWRAP", va='center', fontsize=14, rotation=90)
		ax.text(-60,6.5, "Refinement", va='center', fontsize=14, rotation=90)

		ax.text(-75,1.5, "MetaWRAP", va='center', fontsize=14, rotation=90)
		ax.text(-60,1.5, "Reassembly", va='center', fontsize=14, rotation=90)

	else: plt.yticks([], [])
	
plt.tight_layout(w_pad=0.5)

plt.subplots_adjust(top=0.92, right=0.98, left=0.12, bottom=0.15)
plt.savefig(sys.argv[1],format='eps', dpi=600)
plt.show()





