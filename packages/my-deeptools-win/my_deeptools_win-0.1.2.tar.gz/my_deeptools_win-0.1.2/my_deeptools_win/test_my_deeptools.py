import pybigtools
import bamnostic as bs


def query_chrom_region_signal(
        signal_bam_obj,
        chr_name,
        chr_length,
        scale_method="rpkm",
        binsize=10
):
    """

    :param signal_bam_obj:
    :param chr_name:
    :param chr_length:
    :param scale_method:
    :param binsize:
    :return: generater (chr_name, start, end, signal_value)
    """
    total_count = 0
    for info in signal_bam_obj.get_index_stats():
        total_count += info[0]
    region_count_list = []
    for start in range(38526865, chr_length, binsize):
        end = min(start + binsize, chr_length)
        count = 0
        for read in signal_bam_obj.fetch(chr_name, start, end):
            count += 1
        if scale_method == "cpm":
            count = round(count / total_count * 1e6, 5)
        elif scale_method == "rpkm":
            region_length = end - start + 1
            count = round(count / region_length * 1e3, 5)
        print(end)
        yield (chr_name, start, end, count)

bs_file = bs.AlignmentFile("../data/K562-ATACSeq-rep1.ENCFF534DCE_chr21.bam","rb")
b = pybigtools.open("../data/test.bigWig", "w")
b.write({"chr21": 38530701}, iter(query_chrom_region_signal(bs_file, "chr21", 38530701)))