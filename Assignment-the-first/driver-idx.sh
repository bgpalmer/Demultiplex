#!/usr/bin/env bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --output="file_%j.out"
#SBATCH --error="file_%j.err"
#SBATCH --cpus-per-task=8
#SBATCH --nodes=1



/usr/bin/time -v ./first-idx.py $1