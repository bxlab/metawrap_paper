#!/usr/bin/env python
# USAGE:
# ./script file1.stats file2.stats file3.stats

import sys
import matplotlib.pyplot as plt
plt.switch_backend('agg')

min_completion=50
max_contamination=10

set_list=["refinement_50_1", "refinement_50_2", "refinement_50_4", 
"refinement_50_6", "refinement_50_8", "refinement_50_10", 
"refinement_60_10", "refinement_70_10", "refinement_80_10", 
"refinement_90_10", "refinement_95_10"]

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
plt.figure(figsize=(10, 12))
plt.style.use('ggplot')

pos=0
for data_set in data_sets:
    improvements={}
    for line in open(data_set+"/completion_improvements.txt"):
    	improvements[line.strip().split("\t")[0].split('.')[0]]=line.strip().split("\t")[1]
        
    ####################################################################################################################################
    ############################################             COMPLETION PLOT                ############################################
    ####################################################################################################################################
    pos+=1
    print "plotting completion"
    data={}
    max_x=0
    # loop over all bin .stats files
    for file_name in set_list:
        if file_name.split("_")[-1]!="10": continue
        bin_set=file_name
        data[bin_set]=[]
        for line in open(data_set+"/"+file_name+".stats"):
            # skip header
            if "complete" in line: continue
            # skip bins that are too contaminated or very incomplete
            if float(line.split("\t")[2])>max_contamination: continue
            if float(line.split("\t")[1])<min_completion: continue
            
            # save the completion value of each bin into a list
            data[bin_set].append(float(line.split("\t")[1]))            
            if len(data[bin_set])>max_x: max_x=len(data[bin_set])
            
    # sort the completion data sets
    for bin_set in data:
        data[bin_set].sort(reverse=True)
        
    # Remove the plot frame lines. They are unnecessary chartjunk.    
    ax = plt.subplot(310+pos)
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
            plt.plot(data[bin_set], lw=3.5, color=c)
            x_pos=len(data[bin_set])-1
            y_pos = data[bin_set][x_pos]
            label=">"+bin_set.split("_")[1]+"% [+"+improvements[bin_set]+"]"
            plt.text(x_pos+4, y_pos-1, label, fontsize=18, color=c)
                
    # add plot and axis titles and adjust edges
    if pos<2: plt.title("Bin completion improvement", fontsize=36) 
    plt.ylabel("Bin completion (%)", fontsize=20)
    if pos>2: plt.xlabel("Bin completion ranking", fontsize=20)
    plt.text(-0.17*max_x, 75, data_set, fontsize=30, ha="center", rotation='vertical', verticalalignment='center')


        

# save figure
print "Saving figures binning_results.eps and binning_results.png ..."
plt.tight_layout(w_pad=20)
plt.subplots_adjust(top=0.93, right=0.80, left=0.15, bottom=0.08)
plt.savefig(sys.argv[1],format='eps', dpi=600)
#plt.savefig("binning_results.png",format='png', dpi=600)
#plt.show()






