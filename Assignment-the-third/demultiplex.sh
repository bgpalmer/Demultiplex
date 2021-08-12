#!/usr/bin/bash
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --output="%x_%j.out"
#SBATCH --error="%x_%j.err"
#SBATCH --cpus-per-task=8
#SBATCH --nodes=1

/usr/bin/time -v python3 demultiplex.py \
	--index_file	"/projects/bgmp/shared/2017_sequencing/indexes.txt" \
	--index_1		"/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz" \
	--read_1		"/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz" \
	--index_2		"/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz" \
	--read_2		"/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz" \
	--qscore_cutoff		30.0 \
	--output_dir		$1






