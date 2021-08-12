#!/usr/bin/bash

inputdir="../TEST-input_FASTQ"
outputdir="../TEST-output_FASTQ"


index1_file="${inputdir}/R2_input.fq"
index2_file="${inputdir}/R3_input.fq"
read1_file="${inputdir}/R1_input.fq"
read2_file="${inputdir}/R4_input.fq"

python3 demultiplex.py \
	--index_file	"/projects/bgmp/shared/2017_sequencing/indexes.txt" \
	--index_1		"$index1_file" \
 	--read_1		"$read1_file" \
 	--index_2		"$index2_file" \
 	--read_2		"$read2_file" \
 	--qscore_cutoff		30.0 \
 	--output_dir		${outputdir}

