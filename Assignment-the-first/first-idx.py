#!/usr/bin/env python3


import gzip
import matplotlib.pyplot as plt
import numpy as np
import sys

def convert_phred(letter):
    """Converts a single character into a phred score"""
    return ord(letter) - 33


def file_line_generator(filename: str, n_lines: int = 1) -> None:
    '''
    filename: path to file
    n_lines: number of lines in the list to read
    '''
    fh = gzip.open(filename, 'rb')
    #fh = open(filename, 'rb')
    lines: list = []
    ln: int = 0
    for line in fh:
        ln += 1
        lines.append(line.strip())
        if ln % n_lines == 0:
            yield lines
            lines.clear()
    
    fh.close()


N_LINES_IN_FASTQ_RECORD: int = 4
def get_fastq_records(filename: str):
    '''
    TODO documentation
    '''

    for record in file_line_generator(filename, N_LINES_IN_FASTQ_RECORD):
        yield record


# /projects/bgmp/shared/2017_sequencing/
# /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz
PARENT_DIR='/projects/bgmp/shared/2017_sequencing/'
def populate_list_of_files(files:list):
	for i in range(1,5):
		files.append(f"{PARENT_DIR}1294_S1_L008_R{i}_001.fastq.gz")


# same number of lines in R1-R4
n_records: int = 1452986940 / 4
n_basepairs: int = 101
n_len_idx: int = 8

if "__main__" == __name__:

    filename = sys.argv[1]
    x = np.zeros(n_len_idx, dtype=float)
    for record in get_fastq_records(filename):
        x += [(c - 33) for c in record[3]]

    for i in range(len(x)):
        x[i] /= n_records

    plt.bar([i for i in range(n_len_idx)], x, ec='blue')
    plt.title(f"{filename[filename.rfind('/') + 1:filename.rfind('.')]} Average Quality Score per Base Pair")
    plt.xlabel("Base Pair Position")
    plt.ylabel("Mean Quality Score")
    plt.savefig(f"{filename[filename.rfind('/') + 1:filename.rfind('.')]}.png")

