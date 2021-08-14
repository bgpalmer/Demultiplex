#!/usr/bin/env python3

import bioinfo as bio
import argparse
# import pathlib
# from collections import Counter

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


    # Load indexes into map
    # Key: Sequence (eg. AAAAAAAA)
    # Value: Index Name (eg. F12)
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
    read_counter: dict = {}

    reads = ['R1', 'R4']
    nonmatch_categories = ['Unmatched', 'Unknown']

    # Open file handles for:
    # - Read-Pair Matches
    # - Index hopping ('Unmatched')
    # - Unrecognized indexes, N's in indexes ('Unknown')
    # Total file counts = 52
    #
    # Additionally, initialize counters for all file writes above
    
    for read in reads:
        read_index_match_map[read] = {}
        read_nonmatch_bucket_map[read] = {}

        for index_seq, index_name in index_map.items():
            read_index_match_map[read][index_seq] = open(f"{OUTPUT_DIR}/{read}_{index_name}.fq", 'w')
            read_counter[index_seq] = 0
        for category in nonmatch_categories:
            read_nonmatch_bucket_map[read][category] = open(f"{OUTPUT_DIR}/{read}_{category}.fq", 'w')
            read_counter[category] = 0

    INDEX1_FILE = args.index_1
    INDEX2_FILE = args.index_2
    READ1_FILE = args.read_1
    READ2_FILE = args.read_2
    QUALITY_SCORE_AVG = float(args.qscore_cutoff)


    # Read one record from Read 1-2 and Index 1-2 at a time
    for index1_record, index2_record, read1_record, read2_record in zip(bio.get_fastq_records(INDEX1_FILE), bio.get_fastq_records(INDEX2_FILE), bio.get_fastq_records(READ1_FILE), bio.get_fastq_records(READ2_FILE)):        
        
        # Read2 and Index2 are reverse complemented
        index2_record[1] = bio.reverse_complement(index2_record[1])
        read2_record[1] = bio.reverse_complement(read2_record[1])
        
        # Update read headers with indexes (this assumes files are ordered)
        # Indexes formatting should be 'Index1-Index2 (reverse complemented)''
        read1_record[0] += f" {index1_record[1]}-{index2_record[1]}"
        read2_record[0] += f" {index1_record[1]}-{index2_record[1]}"

        # check the quality of the indexes
        index1_qs: bool = bio.quality_score(index1_record[3]) >= QUALITY_SCORE_AVG
        index2_qs: bool = bio.quality_score(index2_record[3]) >= QUALITY_SCORE_AVG


        '''
        This is where file-writing occurs.
        Additionally, each write per read-pair index
        and nonmatch/unknown categories will be counted.

        Under no circumstance should a read be skipped or not written to a file!!!
        '''

        # Read-Pairs must have known indexes and indexes with good quality scores
        if index2_record[1] in index_map and index1_record[1] in index_map and index1_qs and index2_qs:          
            if index2_record[1] == index1_record[1]:
                read_index_match_map["R1"][index1_record[1]].write('\n'.join(line for line in read1_record) + '\n')
                read_index_match_map["R4"][index2_record[1]].write('\n'.join(line for line in read2_record) + '\n')
                read_counter[index1_record[1]] += 1
            else:
                # If the indexes do not match, write to respective index-hopping files
                read_nonmatch_bucket_map["R1"]["Unmatched"].write('\n'.join(line for line in read1_record) + '\n')
                read_nonmatch_bucket_map["R4"]["Unmatched"].write('\n'.join(line for line in read2_record) + '\n')
                read_counter["Unmatched"] += 1

        else:
            # We did not meet the critera above; update the unknown file
            # Improvement: do not need the if statements...
            if index1_record[1] not in index_map or not index1_qs:
                read_nonmatch_bucket_map["R1"]["Unknown"].write('\n'.join(line for line in read1_record) + '\n')

            if index2_record[1] not in index_map or not index2_qs:
                read_nonmatch_bucket_map["R4"]["Unknown"].write('\n'.join(line for line in read2_record) + '\n')

            read_counter["Unknown"] += 1

    # Close the file handles
    for read in reads:
        for index in index_map.keys():
            read_index_match_map[read][index].close()
        for category in nonmatch_categories:
            read_nonmatch_bucket_map[read][category].close()


    '''
    Output two tables of stats to stdout deliminated with tabs.
    
    Table 1: Read-Pair Match Data
    Headers: 
        - Index: Index Name (eg. F12)
        - Count: Number of index-pair write
        - Percentage: Percentage of total index-pair writes

    Table 2: Reads seen that do not fit Table 1
    Headers:
        - Category: Categories (eg. examples above)
        - Count: Number of values for category
        - Percentage: Percentage of value for ALL reads seens
    '''


    print("Index\tCount\tPercentage")

    total: int = sum(read_counter.values())

    read_count: int = total - read_counter["Unknown"] - read_counter["Unmatched"] 

    for index_seq, index_name in index_map.items():
        print(f"{index_name}\t{read_counter[index_seq]}\t{(read_counter[index_seq]/read_count) * 100:.2f}")

    
    print()
    print("Category\tCount\tPercentage")

    for nonmatch in nonmatch_categories:
        print(f"Read-Pair {nonmatch}\t{read_counter[nonmatch]}\t{(read_counter[nonmatch]/total) * 100:.2f}")

    print(f"Read-Pair Matches\t{read_count}\t{(read_count / total) * 100:.2f}")
    print(f"Total Reads\t{total}\t{(total / total) * 100:.2f}")





        

    


