#!/usr/bin/env Rscript

# 2013-09-16
# works with R 2.15.2 and ggplot 0.9.3.1
# Check ggplot2 help forums or contact sujai.kumar@gmail.com if something doesn't run
# because of updated programs/packages

#Function to ignore low frequency annotations:

clean.blobs<-function(d,threshold,taxlevel) {
    annotated<-d[d[,taxlevel]!="Not annotated",]
    total<-dim(annotated)[1]
    levels(d[,taxlevel])[which(table(d[,taxlevel])<threshold*total)]<-"Not annotated"
    return(d)
}

#########################################################################

#Load data from file and generate plot:

library(ggplot2)
library(reshape2)

subplotwidth=1000;
subplotheight=800;

args <- commandArgs(trailingOnly = TRUE)
arg_input_file <- args[1]
arg_ignore_below_prop=as.numeric(args[2])
arg_taxlevel=args[3]

orig <- read.delim(arg_input_file,header=TRUE,sep="\t")
# change culumn name to be more informative 
colnames(orig)[4] <- strsplit(arg_input_file, "/")[[1]][1]
orig <- orig[orig$len>=200,]

cov_colnames=colnames(orig)[4]
tax_colnames=colnames(orig)[grep("^taxlevel_",colnames(orig))]

numcols=length(cov_colnames)

taxlevel=arg_taxlevel;

# this contains the gc and abund of each point
m<-melt(orig,id.vars=c("seqid","len","gc",taxlevel),measure.vars=cov_colnames, variable.name="read_set", value.name="cov")
mfilt<-clean.blobs(m,arg_ignore_below_prop,taxlevel)
taxnames=names(sort(table(mfilt[,taxlevel]),decreasing=TRUE))
taxnames=c("Not annotated", taxnames[taxnames != "Not annotated"])

# this contains the gc, abund, and taxonomy of each point to plot
mfilt[,taxlevel] <- factor(mfilt[,taxlevel], levels = taxnames)

png(paste(arg_input_file,taxlevel,"png",sep="."), (numcols * subplotwidth), (1 * subplotheight) + 300, units="px",res=100)

theme_set(theme_bw())
paultol=list(c("#DDDDDD") ,c("#DDDDDD","#4477AA"), c("#DDDDDD","#4477AA","#CC6677"), c("#DDDDDD","#4477AA","#DDCC77","#CC6677"), c("#DDDDDD","#4477AA","#117733","#DDCC77","#CC6677"), c("#DDDDDD","#332288","#88CCEE","#117733","#DDCC77","#CC6677"), c("#DDDDDD","#332288","#88CCEE","#117733","#DDCC77","#CC6677","#AA4499"), c("#DDDDDD","#332288","#88CCEE","#44AA99","#117733","#DDCC77","#CC6677","#AA4499"), c("#DDDDDD","#332288","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#CC6677","#AA4499"), c("#DDDDDD","#332288","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#CC6677","#882255","#AA4499"), c("#DDDDDD","#332288","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#661100","#CC6677","#882255","#AA4499"), c("#DDDDDD","#332288","#6699CC","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#661100","#CC6677","#882255","#AA4499"), c("#DDDDDD","#332288","#6699CC","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#661100","#CC6677","#AA4466","#882255","#AA4499"), c("#DDDDDD","#332288","#6699CC","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#661100","#CC6677","#AA4466","#882255","#AA4499","#777777"))
taxa <- c("Not annotated", "Proteobacteria", "Planctomycetes", "Chlorophyta", "Actinobacteria", "Cyanobacteria", "Verrucomicrobia", "Bacteroidetes", "Firmicutes", "Streptophyta", "Chordata", "Ascomycota", "Arthropoda", "Euryarchaeota", "Acidobacteria", "Basidiomycota", "Gemmatimonadetes", "Other")
colors <- c("#DDDDDD","#332288","#6699CC","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#661100","#CC6677","#AA4466","#882255","#AA4499", "#9309f1", "#6B5E74", "#faaa09", "#60c32e", "#777777")


g<-ggplot() + scale_colour_manual(values=colors, name="BLAST annotation", limits=taxa )

for (t in levels(mfilt[,taxlevel])) {
  g <- g + geom_point(data=mfilt[mfilt[,taxlevel]==t,],aes_string(x="gc", y="cov", color=taxlevel), size=2, alpha=I(1/3), show.legend=F)
}
g<-g +
  facet_wrap(~read_set, ncol=numcols) + 
  scale_y_log10(limits=c(5, 10000),breaks = c(1,10,100,1000,10000)) + scale_x_continuous(limits=c(0.2, 0.8),breaks = seq(0,1,.1)) +
  labs(x="GC content", y="Standardized read coverage") + 
  guides(colour = guide_legend(nrow=3, override.aes = list(alpha = 1,size=10))) + 
  theme (
    strip.text.x = element_text(colour = "black", size = 60, vjust = 0.5),
    #strip.background = element_blank(),
    #strip.text.x = element_blank(),
    axis.text.x  = element_text(colour = "black", size = 30, vjust = 1),
    axis.text.y  = element_text(colour = "black", size = 30, vjust = 0.5),
    axis.title.x = element_text(colour = "black", size = 40, vjust = 0),
    axis.title.y = element_text(colour = "black", size = 40, hjust = 0.5, vjust = 0.5, angle=90),
    legend.text  = element_text(colour = "black", size = 18, vjust = 0),
    legend.title = element_text(colour = "black", size = 20, vjust = 0, hjust = 0, lineheight=1),
    legend.justification=c(1,1), legend.position="bottom", legend.direction="horizontal"
  )
g
dev.off()
