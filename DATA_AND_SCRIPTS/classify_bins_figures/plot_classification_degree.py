#!/usr/bin/env python

import sys
import matplotlib.pyplot as plt
plt.switch_backend('agg')


# load in data
data_sets=["Water_taxonomy.tab", "Gut_taxonomy.tab", "Soil_taxonomy.tab"]
data={}
for data_set in data_sets: 
    data[data_set]=[0,0,0,0,0,0,0,0]
    for line in open(data_set):
        data[data_set][0]+=1
        if len(line.strip().split("\t"))==1:
            n_class=1
        else:
            tax=line.strip().split("\t")[1].split(";")
            if "uncultured" in tax[0]: n_class=1
            else: n_class=len(tax)+1
            for i in range(1, n_class):
                 data[data_set][i]+=1        
for k in data:
    print k + "\t" + str(data[k])

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

# set figure size
plt.figure(figsize=(12, 10))
plt.style.use('ggplot')

 
# Remove the plot frame lines. They are unnecessary chartjunk.    
ax = plt.subplot(111)
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
plt.ylim(0, 105)
plt.xlim(0, 5)

# Provide tick lines across the plot to help your viewers trace along    
plt.yticks(range(0, 105, 10), [str(x) for x in range(0, 105, 10)], fontsize=14)    
plt.xticks(fontsize=14)    
for y in range(0, 105, 10):
    plt.plot(range(0, 9), [y] * len(range(0, 9)), "--", lw=0.2, color="black", alpha=0.3, dashes=(15, 15))


n=0
for data_set in data:
    # chose a color!
    c=tableau20[n]
    x=[0,1,2,3,4,5]
    y=[0,0,0,0,0,0]
    for i in range(1, len(data[data_set])-1):
        y[i-1]=100.0*data[data_set][i]/data[data_set][0]
        
    # plot the data
    plt.plot(x, y, lw=3.5, color=c, label=data_set.split("_")[0])
    n+=1
    
    
# add plot and axis titles and adjust edges
plt.title("Bin classification depth", fontsize=30) 
plt.ylabel("Degree of classification (%)", fontsize=20)
plt.xlabel("Taxonomic ranking", fontsize=20)
plt.xticks(x, ["Super-kingdom", "Phylum", "Class", "Family", "Genus", "Species"], rotation=45)

# add legend
legend=plt.legend(bbox_to_anchor=(0.75, 0.65), ncol=1, facecolor=None, prop={'size': 20}, frameon=False, title="Sample", columnspacing=0.5)
legend.get_title().set_fontsize('24')
legend._legend_box.align = "left"

# save figure
plt.subplots_adjust(top=0.90, right=0.95, left=0.12, bottom=0.25)
plt.savefig(sys.argv[1],format='eps', dpi=600)
#plt.savefig("binning_results.png",format='png', dpi=600)
#plt.show()






