#!/usr/bin/env python3

import bioinfo as bio
# import utilities as util
import argparse
import pathlib
from collections import Counter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-idx", "--index_file", type=str, help="indexes")
    parser.add_argument("-i1", "--index_1", type=str, help="index 1")
    parser.add_argument("-r1", "--read_1", type=str, help="read 1")
    parser.add_argument("-i2", "--index_2", type=str, help="index 2")
    parser.add_argument("-r2", "--read_2", type=str, help="read 2")
    parser.add_argument("-qc", "--qscore_cutoff", type=str, help="read average quality score cutoff")
    parser.add_argument("-o", "--output_dir", type=str, help="Output Directory")

    args = parser.parse_args()

    # indexes
    INDEXES = args.index_file

    # output directory
    OUTPUT_DIR = args.output_dir

    # NOTE: the directory should already be made

    # if the output directory does not exits, make it
    # if not os.path.isdir(OUTPUT_DIR):
    #     os.path.mkdir(OUTPUT_DIR)

    index_map: dict = dict()
    with open(INDEXES, 'r') as f:
        ln = 0
        for line in f:
            ln += 1
            if (ln > 1):
                line = line.strip()
                cols = line.split('\t')
                index_map[cols[4]] = cols[3]

    read_index_match_map: dict = {}
    read_nonmatch_bucket_map: dict = {}
    count_map: dict = {}

    reads = ['R1', 'R4']
    nonmatch_categories = ['Unmatched', 'Unknown']

    for read in reads:
        read_index_match_map[read] = {}
        read_nonmatch_bucket_map[read] = {}

        for index_seq, index_name in index_map.items():
            read_index_match_map[read][index_seq] = open(f"{OUTPUT_DIR}/{read}_{index_name}.fq", 'w')
            count_map[index_seq] = 0
        for category in nonmatch_categories:
            read_nonmatch_bucket_map[read][category] = open(f"{OUTPUT_DIR}/{read}_{category}.fq", 'w')
            count_map[category] = 0

    INDEX1_FILE = args.index_1
    INDEX2_FILE = args.index_2
    READ1_FILE = args.read_1
    READ2_FILE = args.read_2
    QUALITY_SCORE_AVG = float(args.qscore_cutoff)


    for index1_record, index2_record, read1_record, read2_record in zip(bio.get_fastq_records(INDEX1_FILE), bio.get_fastq_records(INDEX2_FILE), bio.get_fastq_records(READ1_FILE), bio.get_fastq_records(READ2_FILE)):        
        index2_record[1] = bio.reverse_complement(index2_record[1])
        read2_record[1] = bio.reverse_complement(read2_record[1])
        read1_record[0] += f" {index1_record[1]}-{index2_record[1]}"
        read2_record[0] += f" {index1_record[1]}-{index2_record[1]}"

        # check the quality of the indexes
        index1_qs: bool = bio.quality_score(index1_record[3]) >= QUALITY_SCORE_AVG
        index2_qs: bool = bio.quality_score(index2_record[3]) >= QUALITY_SCORE_AVG

        if index2_record[1] in index_map and index1_record[1] in index_map and index1_qs and index2_qs:          
            if index2_record[1] == index1_record[1]:
                read_index_match_map["R1"][index1_record[1]].write('\n'.join(line for line in read1_record) + '\n')
                read_index_match_map["R4"][index2_record[1]].write('\n'.join(line for line in read2_record) + '\n')
                count_map[index1_record[1]] += 1
            else:
                read_nonmatch_bucket_map["R1"]["Unmatched"].write('\n'.join(line for line in read1_record) + '\n')
                read_nonmatch_bucket_map["R4"]["Unmatched"].write('\n'.join(line for line in read2_record) + '\n')
                count_map["Unmatched"] += 1

        else:
            if index1_record[1] not in index_map or not index1_qs:
                read_nonmatch_bucket_map["R1"]["Unknown"].write('\n'.join(line for line in read1_record) + '\n')

            if index2_record[1] not in index_map or not index2_qs:
                read_nonmatch_bucket_map["R4"]["Unknown"].write('\n'.join(line for line in read2_record) + '\n')

            count_map["Unknown"] += 1


    for read in reads:
        for index in index_map.keys():
            read_index_match_map[read][index].close()
        for category in nonmatch_categories:
            read_nonmatch_bucket_map[read][category].close()



    total_read_pair_matches:int = 0
    print("Index\tCounts")

    for index_seq, index_name in index_map.items():
        print(f"{index_name}\t{count_map[index_seq]}")
        total_read_pair_matches += count_map[index_seq]

    print(f"Read-Pair Matches\t{total_read_pair_matches}")
    for nonmatch in nonmatch_categories:
        print(f"Read-Pair {nonmatch}\t{count_map[nonmatch]}")




        

    


