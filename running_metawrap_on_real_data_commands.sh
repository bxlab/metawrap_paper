#!/usr/bin/env bash
# These are the commands used to process the Soil, Water, and Gut metagenomic sequencing data described in the metaWRAP MS.
# The analysis for these three sets was adentical, so we assume the data is in "RAW_READS"

# read pre-processing, trimming, and human read removal:
tar -xvf RAW_READS/*tar.gz
mkdir READ_QC
for i in RAW_READS/*_1.fastq; do
	metawrap read_qc -1 ${i%_*}_1.fastq -2 ${i%_*}_2.fastq -t 24 -o READ_QC/${i%_*}
done

mkdir CLEAN_READS
for i in READ_QC/*; do 
	b=${i#*/}
	mv ${i}/final_pure_reads_1.fastq CLEAN_READS/${b}_1.fastq
	mv ${i}/final_pure_reads_2.fastq CLEAN_READS/${b}_2.fastq
done

# metagenomic co-assembly of all the samples:
cat CLEAN_READS/*_1.fastq >> CLEAN_READS/ALL_READS_1.fastq
cat CLEAN_READS/*_2.fastq >> CLEAN_READS/ALL_READS_2.fastq
metawrap assembly -1 CLEAN_READS/ALL_READS_1.fastq -2 CLEAN_READS/ALL_READS_2.fastq -m 200 -t 96 -o ASSEMBLY

#running KRAKEN:
metawrap kraken -o KRAKEN -t 96 -s 1000000 CLEAN_READS/*fastq ASSEMBLY/final_assembly.fasta

# initial binning of scaffolds
metawrap binning -o INITIAL_BINNING -t 96 -a ASSEMBLY/final_assembly.fasta --metabat2 --maxbin2 --concoct CLEAN_READS/*fastq

# bin refinemnt (the -c and -x options were changed for various tests, as described in the MS)
metawrap bin_refinement -o BIN_REFINEMENT -t 96 -A INITIAL_BINNING/metabat2_bins/ -B INITIAL_BINNING/maxbin2_bins/ -C INITIAL_BINNING/concoct_bins/ -c 70 -x 10

# bin refinement with Binning_refiner (Binning_refiner is already part of metaWRAP):
cp -r BIN_REFINEMENT/work_files/binsABC Binning_refiner_bins

# bin refinement with DAS_tool:
for bin in INITIAL_BINNING/metabat2_bins//*; do for contig in $(grep ">" $bin); do echo -e "$(echo $contig | cut -d">" -f2)\t$(echo $bin | cut -f2 -d"/")"; done; done > metabat2.tsv
for bin in INITIAL_BINNING/maxbin2_bins//*; do for contig in $(grep ">" $bin); do echo -e "$(echo $contig | cut -d">" -f2)\t$(echo $bin | cut -f2 -d"/")"; done; done > maxbin2.tsv
for bin in INITIAL_BINNING/concoct_bins//*; do for contig in $(grep ">" $bin); do echo -e "$(echo $contig | cut -d">" -f2)\t$(echo $bin | cut -f2 -d"/")"; done; done > concoct.tsv
./DAS_Tool  -i metabat2.tsv, maxbin2.tsv, concoct.tsv --search_engine blast -l metabat2,maxbin2,concoct -c ASSEMBLY/final_assembly.fasta -o DAS_Tool_out

# runnign bin reassembly (the -c and -x options were changed for various tests, as described in the MS):
metawrap reassemble_bins -o BIN_REASSEMBLY -1 CLEAN_READS/ALL_READS_1.fastq -2 CLEAN_READS/ALL_READS_2.fastq -t 96 -m 800 -c 70 -x 10 -b BIN_REFINEMENT/metaWRAP_bins

# bin and contig quantification:
metawrap quant_bins -b BIN_REFINEMENT/metaWRAP_bins -o QUANT_BINS -a ASSEMBLY/final_assemN_READS/*fastq

# running blobology:
metawrap blobology -a ASSEMBLY/final_assembly.fasta -t 96 -o BLOBOLOGY --bins BIN_REFINEMENT/metaWRAP_bins CLEAN_READS/*fastq

# functional annotation:
metawrap annotate_bins -o FUNCT_ANNOT -t 96 -b BIN_REASSEMBLY/reassembled_bins/

# evaluate the bin quality with CheckM:
metaWRAP/bin/metawrap-scripts/checkm.sh DAS_Tool_out
metaWRAP/bin/metawrap-scripts/checkm.sh Binning_refiner_bins
metaWRAP/bin/metawrap-scripts/checkm.sh BIN_REFINEMENT/metaWRAP_bins
metaWRAP/bin/metawrap-scripts/checkm.sh BIN_REASSEMBLY/reassembled_bins
metaWRAP/bin/metawrap-scripts/checkm.sh INITIAL_BINNING/maxbin2_bins
metaWRAP/bin/metawrap-scripts/checkm.sh INITIAL_BINNING/metabat2_bins
metaWRAP/bin/metawrap-scripts/checkm.sh INITIAL_BINNING/concoct_bins

# alternative bin quality assessment of bins in a directory bin_folder with CheckM
checkm lineage_wf -x fa $bin_folder ${bin_folder}.checkm -t 24 --tmpdir ${bin_folder}.tmp

