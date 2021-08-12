import gzip


def file_line_generator(filename: str, n_lines: int = 1) -> None:
    '''
    filename: path to file
    n_lines: number of lines in the list to read
    '''
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
    TODO documentation
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

