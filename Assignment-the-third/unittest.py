import bioinfo as bio

inputdir=r"../TEST-input_FASTQ"
outputdir=r"../TEST-output_FASTQ"

if __name__ == "__main__":

    indexes = set()
    with open(f"{inputdir}/index.txt", 'r') as f:
        for line in f:
            indexes.add(line.strip())