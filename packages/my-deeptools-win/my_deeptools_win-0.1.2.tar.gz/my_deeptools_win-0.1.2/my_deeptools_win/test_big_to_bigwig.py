import pybigtools
chrom_df = {
    "chr1": 248956422,
    "chr2": 242193529,
    "chr3": 198295559,
}
def covert_bigbed_to_bigwig(bigbed_file_path, output_file_path):
        def bigbed_to_bigwig(
                bigbed_file_path
        ):
            f = open(bigbed_file_path)
            for line in f:
                line_list = line.strip().split("\t")
                out_list = (line_list[0], int(line_list[1]), int(line_list[2]), float(line_list[3]))
                yield out_list
            f.close()

        b = pybigtools.open(output_file_path, "w")
        b.write(chrom_df, bigbed_to_bigwig(bigbed_file_path))

if __name__ == "__main__":
    covert_bigbed_to_bigwig("../data/293.ChIP.H3K36me3.rep1.ENCFF899GOH.bedGraph", "../data/test.bw")