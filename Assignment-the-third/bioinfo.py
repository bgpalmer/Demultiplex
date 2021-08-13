import gzip


def file_line_generator(filename: str, n_lines: int = 1) -> None:
    '''
    filename: path to file
    n_lines: number of lines in the list to read
    '''


    # NOTE: use standard open for unittest.sh!!!

    fh = gzip.open(filename, 'rt')
    #fh = open(filename, 'r')
    lines: list = []
    lc = 0
    for line in fh:
        lc += 1
        lines.append(line.strip())
        if lc % n_lines == 0:
            yield lines
            lines.clear()
    
    fh.close()


N_LINES_IN_FASTQ_RECORD: int = 4
def get_fastq_records(filename: str):
    '''
    Wrapper function to get fastq record
    This function returns 4 lines at a time
    '''

    for record in file_line_generator(filename, N_LINES_IN_FASTQ_RECORD):
        yield record


dNTP_pairing: dict = { 
    'A': 'T', 
    'T': 'A', 
    'G': 'C', 
    'C': 'G' 
}

def reverse_complement(sequence:str):
    """Returns reverse complement of sequence"""
    return "".join([dNTP_pairing.get(c, 'N') for c in sequence[::-1]])


def convert_phred(letter):
    """Converts a single character into a phred score"""
    return ord(letter) - 33


def quality_score(phred_score:str):
    """ Returns quality score calculation """
    s = 0
    for c in phred_score:
        s += convert_phred(c)
    return s / len(phred_score)


# An attempt to get the best match...

# def get_best_match(indexes: map, target: str, ) -> tuple
#     """return a list of tuples with best scores"""

#     target_len: int = len(target)

#     if target in indexes:
#         return target, target_len, quality_score(target)

#     x = np.zeros((target_len + 1, target_len + 1), dtype=int)

#     best_match_index = None
#     best_match_score: int = 0
#     secondary_score: float = 0.0

#     for index in indexes:
#         for i, t in enumerate(target):
#             for j, c in enumerate(index):
#                 x[i + 1][j + 1] = max(x[i + 1][t], x[i][t + 1]) + int(c == t)

#         if x[target_len][target_len] >= best_match_score:
#             target.count('N') > 1




