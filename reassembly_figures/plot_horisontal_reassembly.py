#!/usr/bin/env python
# USAGE:
# ./script file1.stats file2.stats file3.stats

import sys
import matplotlib.pyplot as plt
plt.switch_backend('agg')

min_completion=50
max_contamination=10

set_list=["metaWRAP", "metaWRAP-reassembled"]
data_sets=["Water", "Gut", "Soil"]


# set some color schemes
tableau20 = [(214, 39, 40), (31, 119, 180), (255, 127, 14), 
             (44, 160, 44), (255, 15, 150), (197, 176, 213), 
             (140, 86, 75), (196, 156, 148), (227, 119, 194), 
             (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), 
             (158, 218, 229)]
             
for i in range(len(tableau20)):    
	r, g, b = tableau20[i]    
	tableau20[i] = (r / 255., g / 255., b / 255.)
plot_colors={}
for i, bin_set in enumerate(set_list): plot_colors[bin_set]=tableau20[i]
# set figure size
plt.figure(figsize=(20, 13))
plt.style.use('ggplot')

pos=0
for data_set in data_sets:
    ####################################################################################################################################
    ############################################             COMPLETION PLOT                ############################################
    ####################################################################################################################################
    pos+=1
    print "plotting completion"
    data={}
    max_x=0
    # loop over all bin .stats files
    for file_name in set_list:
        bin_set=file_name
        data[bin_set]=[]
        for line in open(data_set+"/"+file_name+".stats"):
            # skip header
            if "completeness" in line: continue
            # skip bins that are too contaminated or very incomplete
            if float(line.split("\t")[2])>1.0*max_contamination: continue
            if float(line.split("\t")[1])<1.0*min_completion: continue
            # save the completion value of each bin into a list
            
            data[bin_set].append(float(line.split("\t")[1]))
            if len(data[bin_set])>max_x: max_x=len(data[bin_set])
            
    # sort the completion data sets
    for bin_set in data:
        data[bin_set].sort(reverse=True)
        
    # Remove the plot frame lines. They are unnecessary chartjunk.    
    ax = plt.subplot(330+pos)
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
        plt.yticks(range(min_completion, 105, 10), [str(x) for x in range(min_completion, 105, 10)], fontsize=14)    
        plt.xticks(fontsize=14)    
        
        # Provide tick lines across the plot to help your viewers trace along    
        for y in range(min_completion, 105, 10):    
            plt.plot(range(0, max_x), [y] * len(range(0, max_x)), "--", lw=0.2, color="black", alpha=0.3, dashes=(15, 15))
            
        # Remove the tick marks; they are unnecessary with the tick lines we just plotted.    
        plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")    
            
            
    # start plotting data
    for bin_set in data:
        # chose a color!
        c=plot_colors[bin_set]
        
        # plot the data
        if pos==3:
            if bin_set=="MaxBin2" or bin_set=="metaBAT2" or bin_set=="CONCOCT": plt.plot(data[bin_set], lw=3.5, color=c, linestyle='dashed', label=bin_set)
            else: plt.plot(data[bin_set], lw=3.5, color=c)
        else:
            if bin_set=="MaxBin2" or bin_set=="metaBAT2" or bin_set=="CONCOCT": plt.plot(data[bin_set], lw=3.5, color=c, linestyle='dashed')
            else: plt.plot(data[bin_set], lw=3.5, color=c)
        
    # add plot and axis titles and adjust edges
    plt.title(data_set, fontsize=30) 
    #if pos==1: plt.ylabel("Bin completion (%)", fontsize=20)
    #plt.xlabel("Bin completion ranking", fontsize=20)
    if pos==1: plt.text(-0.18*max_x, 75, "Completion %", fontsize=30, ha="center", rotation='vertical', verticalalignment='center')



for data_set in data_sets:
    ####################################################################################################################################
    ############################################            CONTAMINATION PLOT              ############################################
    ####################################################################################################################################
    print "Plotting contamination..."
    pos+=1
    data={}
    # loop over all bin .stats files
    for file_name in set_list:
        bin_set=file_name
        data[bin_set]=[]
        for line in open(data_set+"/"+file_name+".stats"):
            # skip header
            if "completeness" in line: continue
            
            # skip bins that are too incomplete or way too contaminated
            if line.split("\t")[1]=="NA": continue
            if float(line.split("\t")[1])<1.0*min_completion: continue
            if float(line.split("\t")[2])>1.0*max_contamination: continue
            # save the contamination value of each bin into a list
            data[bin_set].append(float(line.split("\t")[2]))
            
            # sort the contamination data sets
    for bin_set in data:
        data[bin_set].sort(reverse=False)
        
    # MAKING THE PLOT PRETTY!!!!
    ax = plt.subplot(330+pos)
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
    plt.ylim(0, max_contamination+1)
    #ax.set_yscale('log')
    max_x=0
    for k in data:
        if len(data[k])>max_x: max_x=len(data[k])
        plt.xlim(0, max_x)
        
        # Make sure your axis ticks are large enough to be easily read.    
        plt.yticks(range(0, max_contamination+2, 2), [str(x) for x in range(0, max_contamination+2, 2)], fontsize=14)
        plt.xticks(fontsize=14)    
        
        # Provide tick lines across the plot to help your viewers trace along    
        for y in range(0, max_contamination+2, 2):
            plt.plot(range(0, max_x), [y] * len(range(0, max_x)), "--", lw=0.2, color="black", alpha=0.3, dashes=(15, 15))    
            
    # Remove the tick marks; they are unnecessary with the tick lines we just plotted.    
    plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")    
    
        
    # start plotting data
    for bin_set in data:
    # chose a color!
        c=plot_colors[bin_set]

        if pos==6:
            if bin_set=="MaxBin2" or bin_set=="metaBAT2" or bin_set=="CONCOCT": plt.plot(data[bin_set], lw=3.5, color=c, linestyle='dashed')
            else: plt.plot(data[bin_set], lw=3.5, color=c, label=bin_set)
        else:
            if bin_set=="MaxBin2" or bin_set=="metaBAT2" or bin_set=="CONCOCT": plt.plot(data[bin_set], lw=3.5, color=c, linestyle='dashed')
            else: plt.plot(data[bin_set], lw=3.5, color=c)
               
    # add plot and axis titles and adjust the edges
    #if pos==4: plt.ylabel("Bin contamination (%)", fontsize=20)
    plt.gcf().subplots_adjust(right=0.9)
    #plt.xlabel("Bin ranking", fontsize=20)
    if pos==4: plt.text(-0.18*max_x, 5, "Contamination %", fontsize=30, ha="center", rotation='vertical', verticalalignment='center')
    


for data_set in data_sets:
    ####################################################################################################################################
    ############################################             N50 PLOT                ############################################
    ####################################################################################################################################
    pos+=1
    print "plotting N50"
    data={}
    max_x=0
    max_n50=0
    # loop over all bin .stats files
    for file_name in set_list:
        bin_set=file_name
        data[bin_set]=[]
        for line in open(data_set+"/"+file_name+".stats"):
            # skip header
            if "complete" in line: continue
            # skip bins that are too contaminated or very incomplete
            if float(line.split("\t")[2])>max_contamination: continue
            if float(line.split("\t")[1])<min_completion: continue
            
            # save the completion value of each bin into a list
            data[bin_set].append(float(line.split("\t")[5]))            
            if len(data[bin_set])>max_x: max_x=len(data[bin_set])
            if int(line.split("\t")[5])>max_n50: max_n50=int(line.split("\t")[5])
            
    # sort the completion data sets
    for bin_set in data:
        data[bin_set].sort(reverse=True)
        
    # Remove the plot frame lines. They are unnecessary chartjunk.    
    ax = plt.subplot(330+pos)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_linewidth(0.5)
    ax.spines['bottom'].set_color('black')
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_facecolor('white')
    ax.set_yscale('log')
    
    # Ensure that the axis ticks only show up on the bottom and left of the plot.    
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    
    # Limit the range of the plot to only where the data is.    
    max_x=0
    plt.ylim(1000, 2000000)
    for k in data:
        if len(data[k])>max_x: max_x=len(data[k])
        plt.xlim(0, max_x)
    
        # Make sure your axis ticks are large enough to be easily read.    
        plt.yticks([1000,10000,100000,1000000], ["1","10","100","1000"], fontsize=14) 
        plt.xticks(fontsize=14)    
        
        # Provide tick lines across the plot to help your viewers trace along    
        for y in [1000,10000,100000,1000000]:
        	plt.plot(range(0, max_x), [y] * len(range(0, max_x)), "--", lw=0.2, color="black", alpha=0.3, dashes=(15, 15))    
                    
        # Remove the tick marks; they are unnecessary with the tick lines we just plotted.    
        plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")    
            
            
        # start plotting data
    for bin_set in data:
        # chose a color!
        c=plot_colors[bin_set]
        
        # plot the data
        if bin_set=="MaxBin2" or bin_set=="metaBAT2" or bin_set=="CONCOCT": plt.plot(data[bin_set], lw=3.5, color=c, linestyle='dashed')
        else: plt.plot(data[bin_set], lw=3.5, color=c, label=bin_set)
        
        
    # add plot and axis titles and adjust edges
    #if pos<3: plt.title("Bin N50", fontsize=36) 
    #plt.ylabel("Bin N50 (Kbp)", fontsize=20)
    plt.xlabel("Bin completion ranking", fontsize=20)
    if pos==7: plt.text(-0.18*max_x, 50000, "N50", fontsize=30, ha="center", rotation='vertical', verticalalignment='center')
    
    if pos==8: 
        legend=plt.legend(bbox_to_anchor=(1.5, -0.2), ncol=2, facecolor=None, prop={'size': 30}, frameon=False, title=None, columnspacing=0.5)
        legend.get_title().set_fontsize('24')
        legend._legend_box.align = "left"

    

# save figure
print "Saving figures..."
plt.tight_layout(w_pad=5)
plt.subplots_adjust(top=0.95, right=0.97, left=0.08, bottom=0.12)
plt.savefig(sys.argv[1],format='eps', dpi=600)
#plt.savefig("binning_results.png",format='png', dpi=600)
#plt.show()






