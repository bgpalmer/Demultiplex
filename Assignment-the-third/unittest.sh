#!/usr/bin/bash

inputdir="../TEST-input_FASTQ"
expectdir="../TEST-output_FASTQ"
actualdir="./${1}"

#function die
#{
#	echo "MISMATCH FOUND $1"
	# exit 1
#}

mkdir $actualdir

index1_file="${inputdir}/R2_input.fq.gz"
index2_file="${inputdir}/R3_input.fq.gz"
read1_file="${inputdir}/R1_input.fq.gz"
read2_file="${inputdir}/R4_input.fq.gz"

python3 demultiplex.py \
	--index_file	"/projects/bgmp/shared/2017_sequencing/indexes.txt" \
	--index_1		"$index1_file" \
 	--read_1		"$read1_file" \
 	--index_2		"$index2_file" \
 	--read_2		"$read2_file" \
 	--qscore_cutoff		30.0 \
 	--output_dir		${actualdir}

# diff files 
ls -1 $actualdir | while read line; do diff "${actualdir}/${line}" "${expectdir}/${line}"; done

exit 0