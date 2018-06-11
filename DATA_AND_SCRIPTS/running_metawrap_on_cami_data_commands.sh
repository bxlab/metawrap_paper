#!/usr/bin/env bash
# These are the commands used to process the CAMI low, medium, and high metagenomic binning challenge data described in the metaWRAP MS.
# The analysis for these three sets was adentical, so we assume the reads are in RAW_READS, and the gold standard assmebly is ASSEMBLY.fa, the gold standard binnig file is in binning_gold_standard.tab, and 

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

# initial binning of scaffolds
metawrap binning -o INITIAL_BINNING -t 96 -a ASSEMBLY.fa --metabat2 --maxbin2 --concoct CLEAN_READS/*fastq

# bin refinemnt with metaWRAP (the -c and -x options were changed for various tests, as described in the MS):
metawrap bin_refinement -o BIN_REFINEMENT -t 96 -A INITIAL_BINNING/metabat2_bins/ -B INITIAL_BINNING/maxbin2_bins/ -C INITIAL_BINNING/concoct_bins/ -c 70 -x 10

# bin refinement with Binning_refiner (Binning_refiner is already part of metaWRAP):
cp -r BIN_REFINEMENT/work_files/binsABC Binning_refiner_bins

# bin refinement with DAS_tool:
for bin in INITIAL_BINNING/metabat2_bins/*; do for contig in $(grep ">" $bin); do echo -e "$(echo $contig | cut -d">" -f2)\t$(echo $bin | cut -f2 -d"/")"; done; done > metabat2.tsv
for bin in INITIAL_BINNING/maxbin2_bins/*; do for contig in $(grep ">" $bin); do echo -e "$(echo $contig | cut -d">" -f2)\t$(echo $bin | cut -f2 -d"/")"; done; done > maxbin2.tsv
for bin in INITIAL_BINNING/concoct_bins/*; do for contig in $(grep ">" $bin); do echo -e "$(echo $contig | cut -d">" -f2)\t$(echo $bin | cut -f2 -d"/")"; done; done > concoct.tsv
./DAS_Tool  -i metabat2.tsv, maxbin2.tsv, concoct.tsv --search_engine blast -l metabat2,maxbin2,concoct -c ASSEMBLY/final_assembly.fasta -o DAS_Tool_out


# bin quality assessment with AMBER

python3 AMBER/src/utils/convert_fasta_bins_to_cami.py INITIAL_BINNING/metabat2_bins/* -o metabat2.csv
python3 AMBER/src/utils/convert_fasta_bins_to_cami.py INITIAL_BINNING/maxbin2/* -o maxbin2.csv
python3 AMBER/src/utils/convert_fasta_bins_to_cami.py INITIAL_BINNING/concoct/* -o concoct.csv
python3 AMBER/src/utils/convert_fasta_bins_to_cami.py BIN_REFINEMENT/metaWRAP_bins/* -o metawrap.csv
python3 AMBER/src/utils/convert_fasta_bins_to_cami.py DAS_tool_bins/* -o das_tool.csv
python3 AMBER/src/utils/convert_fasta_bins_to_cami.py Binning_refiner_bins/* -o refiner.csv


python3 amber.py -l "MaxBin2, CONCOCT, MetaBAT, metaWRAP, DAS_tool, Binning_refiner" \
-f ASSEMBLY.fa -g binning_gold_standard.tab -k "circular element" \
metabat2.scv concoct_bins.csv metabat2_bins.csv metawrap.csv das_tool.csv refiner.csv \
-o AMBER_OUT




