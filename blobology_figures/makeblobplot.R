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

multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  require(grid)

  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)

  numPlots = length(plots)

  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                    ncol = cols, nrow = ceiling(numPlots/cols))
  }

 if (numPlots==1) {
    print(plots[[1]])

  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))

    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))

      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}

plot_bin_set <-function (file, out) {
  arg_input_file <- file
  arg_ignore_below_prop=0.00001
  arg_taxlevel="bin"

  orig <- read.delim(arg_input_file,header=TRUE,sep="\t")
  # change culumn name to be more informative 
  colnames(orig)[4] <- paste("\n", strsplit(arg_input_file, "/")[[1]][1], " Bins", "\n", sep="")
  orig <- orig[orig$len>=200,]

  cov_colnames=colnames(orig)[4]
  numcols=length(cov_colnames)
  taxlevel=arg_taxlevel;

  # this contains the gc and abund of each point
  m<-melt(orig,id.vars=c("seqid","len","gc",taxlevel),measure.vars=cov_colnames, variable.name="read_set", value.name="cov")
  mfilt<-clean.blobs(m,arg_ignore_below_prop,taxlevel)
  taxnames=names(sort(table(mfilt[,taxlevel]),decreasing=TRUE))
  taxnames=c("Unbinned", taxnames[taxnames != "Unbinned"])

  # this contains the gc, abund, and taxonomy of each point to plot
  mfilt[,taxlevel] <- factor(mfilt[,taxlevel], levels = taxnames)

  png(out, (numcols * subplotwidth), (1 * subplotheight) + 300, units="px",res=100)

  theme_set(theme_bw())
  random_colors=c("#DDDDDD", "#FA5F70", "#BB24F7", "#EA9143", "#E83EEE", "#E1EE3C", "#70945B", "#CC6B80", "#6B98F3", "#4EB175", "#3EED21", "#916B1A", "#377C4A", "#41BE37", "#F1A9D1", "#71128D", "#01545D", "#35ADC2", "#668A25", "#8BBBF0", "#07E3AE", "#424CDD", "#A7E0A5", "#0A3DC8", "#135826", "#D7304B", "#BE272F", "#ACB103", "#8A1379", "#FB3514", "#999C2A", "#865E66", "#51264C", "#CD05D9", "#57C2F6", "#92B719", "#A98421", "#B40324", "#79B7A0", "#0B3AB7", "#48C323", "#8830D5", "#1E87AA", "#E08E36", "#87AF8F", "#326AFB", "#4C2070", "#ADD98F", "#61FB2E", "#561763", "#DD1E39", "#38392D", "#1BFF29", "#27AC47", "#227A8D", "#AD18C8", "#D19B92", "#DC0577", "#920030", "#ECC6E9", "#BB113A", "#FD76CC", "#7FB5BF", "#EED2B9", "#D6C4DF", "#CB038A", "#3A47AB", "#403F32", "#B75F64", "#7449BA", "#A8BCAF", "#A4DB10", "#7389CE", "#64AA81", "#DE44BB", "#E03223", "#6D234A", "#0124DA", "#FB9E40", "#36221C", "#B42BEF", "#09BCFB", "#65002E", "#5E0AEA", "#5F1274", "#2B7A8C", "#28813E", "#1368B0", "#8DD870", "#F997F9", "#C6C160", "#5FE146", "#BE4647", "#6E195D", "#6C170C", "#93847A", "#4A4E74", "#FD1D18", "#17DFE1", "#4AA396", "#FC3808", "#1F6927", "#AE30C5", "#3F3448", "#78033B", "#98F193", "#38B5EC", "#C2A8BF", "#247C44", "#F4D97E", "#38EF04", "#720E56", "#BC7641", "#DC0064", "#9B5D15", "#FC1E5E", "#DD3717", "#D56288", "#21D33F", "#6DFA34", "#725B55", "#9BAB64", "#DF87C5", "#4B362F", "#262D38", "#B90334", "#3AFF6F", "#0CD849", "#7B781B", "#AB846F", "#B2A7CF", "#070416", "#7D9327", "#ACE44C", "#D2997C", "#9F37EB", "#F34C0F", "#4BB029", "#A1A644", "#BFAB1C", "#5E6607", "#E1E978", "#08E708", "#32FBE1", "#54CF23", "#72750C", "#527ABC", "#88540E", "#0DB5D7", "#4D4278", "#D3DC09", "#E60907", "#F2170D", "#C56456", "#AD71B2", "#B2AE04", "#C3F4ED", "#8185AA", "#576248", "#4C39AA", "#8EA094", "#D22FC5", "#65337A", "#C1421F", "#64C3AC", "#BEEA78", "#B55186", "#203930", "#901115", "#234E7B", "#E58256", "#C5007B", "#BB6654", "#E77D9D", "#01EBC3", "#0D2C2F", "#1E759D", "#3C81D8", "#99283D", "#2BEEC2", "#EDC71A", "#82BA30", "#649623", "#302FD9", "#F1CCBD", "#70BC8A", "#610062", "#5F6845", "#426926", "#34D602", "#A44312", "#5F6895", "#1F7780", "#3B43EF", "#16A94E", "#FE12A7", "#D03C65", "#CA1F26", "#ACD36F", "#7E2048", "#352A79", "#777777")
  n <-length(levels(mfilt[,taxlevel]))
  colors_new <- random_colors[c(1:n)]

  g<-ggplot() + scale_colour_manual(values=colors_new, name="Bin annotation", limits=levels(mfilt[,taxlevel]) )

  # plot points
  for (t in levels(mfilt[,taxlevel])) {
    g <- g + geom_point(data=mfilt[mfilt[,taxlevel]==t,],aes_string(x="gc", y="cov", colour=taxlevel), size=2, alpha=I(1/3), show.legend=F)
  }
  # sets styling
  g<-g +
    facet_wrap(~read_set, ncol=numcols) + 
    scale_y_log10(limits=c(5, 10000),breaks = c(1,10,100,1000,10000)) + scale_x_continuous(limits=c(0.2, 0.8),breaks = seq(0,1,.2)) +
    labs(x="GC content", y="Contig abundance") + 
    guides(colour = guide_legend(nrow=3, override.aes = list(alpha = 1,size=10))) + 
    theme (
      strip.text.x = element_text(colour = "black", size = 60, vjust = 0.5, lineheight=0.1),
      #strip.background = element_blank(),
      #strip.text.x = element_blank(),
      axis.text.x  = element_text(colour = "black", size = 40, vjust = 1),
      axis.text.y  = element_text(colour = "black", size = 40, vjust = 0.5),
      axis.title.x = element_text(colour = "black", size = 40, vjust = 0),
      axis.title.y = element_text(colour = "black", size = 40, hjust = 0.5, vjust = 0.5, angle=90),
      plot.margin = unit(c(1,0.5,2,0.5), "lines"),
      legend.justification=c(1,1), legend.position="bottom", legend.direction="horizontal"
    )
  return(g)
}

plot_data_set <-function (file, out) {
  arg_input_file <- file
  arg_ignore_below_prop=0.005
  arg_taxlevel="taxlevel_phylum"

  orig <- read.delim(arg_input_file,header=TRUE,sep="\t")
  # change culumn name to be more informative 
  colnames(orig)[4] <- paste("\n", strsplit(arg_input_file, "/")[[1]][1], " Phyla", "\n", sep="")
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

  png(out, (numcols * subplotwidth), (1 * subplotheight) + 300, units="px",res=100)

  theme_set(theme_bw())
  paultol=list(c("#DDDDDD") ,c("#DDDDDD","#4477AA"), c("#DDDDDD","#4477AA","#CC6677"), c("#DDDDDD","#4477AA","#DDCC77","#CC6677"), c("#DDDDDD","#4477AA","#117733","#DDCC77","#CC6677"), c("#DDDDDD","#332288","#88CCEE","#117733","#DDCC77","#CC6677"), c("#DDDDDD","#332288","#88CCEE","#117733","#DDCC77","#CC6677","#AA4499"), c("#DDDDDD","#332288","#88CCEE","#44AA99","#117733","#DDCC77","#CC6677","#AA4499"), c("#DDDDDD","#332288","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#CC6677","#AA4499"), c("#DDDDDD","#332288","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#CC6677","#882255","#AA4499"), c("#DDDDDD","#332288","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#661100","#CC6677","#882255","#AA4499"), c("#DDDDDD","#332288","#6699CC","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#661100","#CC6677","#882255","#AA4499"), c("#DDDDDD","#332288","#6699CC","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#661100","#CC6677","#AA4466","#882255","#AA4499"), c("#DDDDDD","#332288","#6699CC","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#661100","#CC6677","#AA4466","#882255","#AA4499","#777777"))
  taxa <- c("Not annotated", "Proteobacteria", "Planctomycetes", "Chlorophyta", "Actinobacteria", "Cyanobacteria", "Verrucomicrobia", "Bacteroidetes", "Firmicutes", "Streptophyta", "Chordata", "Ascomycota", "Arthropoda", "Euryarchaeota", "Acidobacteria", "Basidiomycota", "Gemmatimonadetes", "Other")
  colors <- c("#DDDDDD","#332288","#6699CC","#88CCEE","#44AA99","#117733","#999933","#DDCC77","#661100","#CC6677","#AA4466","#882255","#AA4499", "#9309f1", "#6B5E74", "#faaa09", "#60c32e", "#777777")

  # sets colors and legend
  g<-ggplot() + scale_colour_manual(values=colors, name="BLAST annotation", limits=taxa )

  # plot points
  for (t in levels(mfilt[,taxlevel])) {
    g <- g + geom_point(data=mfilt[mfilt[,taxlevel]==t,],aes_string(x="gc", y="cov", color=taxlevel), size=2, alpha=I(1/3), show.legend=T)
  }

  # sets styling
  g<-g +
    facet_wrap(~read_set, ncol=numcols) + 
    scale_y_log10(limits=c(5, 10000),breaks = c(1,10,100,1000,10000)) + scale_x_continuous(limits=c(0.2, 0.8),breaks = seq(0,1,.2)) +
    labs(x="GC content", y="Contig abundance") + 
    guides(colour = guide_legend(nrow=3, override.aes = list(alpha = 1,size=10))) + 
    theme (
      strip.text.x = element_text(colour = "black", size = 60, vjust = 0.5, lineheight=0.1),
      #strip.background = element_blank(),
      #strip.text.x = element_blank(),
      axis.text.x  = element_text(colour = "black", size = 40, vjust = 1),
      axis.text.y  = element_text(colour = "black", size = 40, vjust = 0.5),
      axis.title.x = element_text(colour = "black", size = 40, vjust = 0),
      axis.title.y = element_text(colour = "black", size = 40, hjust = 0.5, vjust = 0.5, angle=90),
      legend.text  = element_text(colour = "black", size = 30, vjust = 0),
      legend.title = element_text(colour = "black", size = 35, vjust = 0, hjust = 0, lineheight=1),
      plot.margin = unit(c(1,0.5,3,0.5), "lines"),
      legend.key.width = unit(2, "cm"),
      legend.justification=c(1,1), legend.position="bottom", legend.direction="horizontal"
    )
  return(g)
}


#########################################################################

#Load data from file and generate plot:

library(ggplot2)
library(reshape2)
library(gridExtra)
library(cowplot)
library(gtable)
library(grid)

subplotwidth=3000;
subplotheight=1200;

args <- commandArgs(trailingOnly = TRUE)

# plot phylum
g1 <- plot_data_set("Water/long_3kb.blobplot", args[1])
g2 <- plot_data_set("Gut/long_3kb.blobplot", args[1])
g3 <- plot_data_set("Soil/long_3kb.blobplot", args[1])

# plot bins
b1 <- plot_bin_set("Water/long_3kb.blobplot", args[1])
b2 <- plot_bin_set("Gut/long_3kb.blobplot", args[1])
b3 <- plot_bin_set("Soil/long_3kb.blobplot", args[1])

# remove redundant labels
g2 <- g2 + theme(axis.text.y = element_blank(), axis.title.y = element_blank())
g3 <- g3 + theme(axis.text.y = element_blank(), axis.title.y = element_blank())
b2 <- b2 + theme(axis.text.y = element_blank(), axis.title.y = element_blank())
b3 <- b3 + theme(axis.text.y = element_blank(), axis.title.y = element_blank())

# add legend
legend <- get_legend(g1 + theme(legend.position="bottom"))
g1 <- g1 + theme(legend.position="none")
g2 <- g2 + theme(legend.position="none")
g3 <- g3 + theme(legend.position="none")
blank <- grid.rect(gp=gpar(col="white"))


#p <- plot_grid( prow, legend_b, ncol = 1, rel_heights = c(1, .2))

layout=matrix(c(1,2,3,4,4,5,6,7,8), nrow=3, byrow=TRUE)
top_row <- grid.arrange(g1, g2, g3, ncol=3, widths=c(2, 1.7, 1.7))
bot_row <- grid.arrange(b1, b2, b3, ncol=3, widths=c(2, 1.7, 1.7))
legend_row <- grid.arrange(legend, blank, ncol=2, widths=c(1, 0.05))
#plot_grid(top_row, legend_row, align = "h", ncol = 1, rel_heights = c(2, 0.3))
plot_grid(bot_row, align = "h", ncol = 1, rel_heights = c(2))
#plot_grid(top_row, legend_row, bot_row, align = "h", ncol = 1, rel_heights = c(2, 0.3, 2))


dev.off()




