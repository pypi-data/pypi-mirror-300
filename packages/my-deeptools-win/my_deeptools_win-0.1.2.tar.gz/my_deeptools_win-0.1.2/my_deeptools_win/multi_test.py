import numpy as np
import bamnostic as bs
import pybigtools
# from my_deeptools_win import set_logging_level
# from rich.progress import track
import logging
from rich.logging import RichHandler
from rich.console import Console
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")


def query_target_region_bin(
        bam_file_path,
        region_list,
        binsize = 10,
        scale_method = "cpm"
)-> np.array :
    """
    :param bam_obj: bam object
    :param region_list: list of (chr, start, end)
    :param binsize: bin size
    :return: numpy array of coverage
    """
    bam_obj = bs.AlignmentFile(bam_file_path, "rb")
    total_align_count = 0

    for bam_index_info in bam_obj.get_index_stats():
        # ref_name = bam_index_info[0]
        map_count = bam_index_info[0]

        total_align_count += map_count
    coverage = np.zeros(int((region_list[2] - region_list[1]) / binsize))
    chr_name = region_list[0]
    start, end = region_list[1], region_list[2]
    # print("chr:", chr_name)
    #print("start:", start)
    big_list = []
    for read in bam_obj.fetch(chr_name, start, end):
        coverage[int((read.reference_start-region_list[1])/binsize):int((read.reference_end-region_list[1]) /binsize)] += 1.0
    if scale_method == "count":
        coverage = coverage
    elif scale_method == "cpm":
        coverage = coverage / total_align_count * 1e6
    elif scale_method == "rpkm":
        coverage = coverage / (total_align_count * binsize) * 1e6

    #print(len(coverage))
    for i in range(coverage.shape[0]):
        start_in = start +  binsize
        big_list.append((chr_name, start, start_in, float(coverage[i])))
        start = start_in
    return big_list


# bs_file = bs.AlignmentFile("../data/293.ChIP.H3K36me3.rep1.ENCFF899GOH.bam","rb")
from multiprocessing import Pool
# chr_length_dt = {
#     "chr1": 248956422,
#     "chr2": 242193529,
#     "chr3": 198295559,
#     "chr4": 190214555,
#     "chr5": 181538259,
#     "chr6": 170805979,
#     "chr7": 159345973,
#     "chr8": 145138636,
# }
# chr_length_dt = {
#     "chr1": 248956422,
#     "chr2": 242193529,
#     "chr3": 198295559,
# }
# thread = 10
import time
def convert_bam_to_bigbed(bam_file_path, output_file_path,genome_dt,thread,binsize,scale_method):
    genome_file = open(genome_dt)
    chr_length_dt = {}
    for line in genome_file:
        line_list = line.strip().split("\t")
        chr_length_dt[line_list[0]] = int(line_list[1])
    genome_file.close()
    for index_num,chr_name in enumerate(chr_length_dt):
        log.info(f"start {chr_name}")
        start_time = time.time()

        pool = Pool(processes=thread)
        chr_bins = int(chr_length_dt[chr_name] / binsize)
        coverage_list = []
        for i in range(thread):
            coverage_list.append(pool.apply_async(query_target_region_bin, args=(
            bam_file_path,[chr_name, int(i * chr_bins / thread) * binsize, int((i + 1) * chr_bins / thread) * binsize],binsize,scale_method)))

        pool.close()
        pool.join()
        merge_total_count_list = []
        for temp_index, res in enumerate(coverage_list):
            run_res = res.get()
            # print(run_res)
            merge_total_count_list.append(run_res)
        if index_num == 0:
            f = open(output_file_path , "w")
        else:
            f = open(output_file_path , "a")
        for temp_index, res in enumerate(merge_total_count_list):
            # print(res)
            for temp_index, res in enumerate(res):
                # print(res)
                f.write(str(res[0]) + "\t" + str(res[1]) + "\t" + str(res[2]) + "\t" + str(res[3]) + "\n")
        # print(chr_name)
        # print(start_time)
        total_time = round((time.time() - start_time) / 60,2)
        log.info(f"convert {chr_name} time: {total_time}")
        # index_num += 1
        # print(f"convert {chr_name} time:", (time.time() - start_time) / 60)
        f.close()
def covert_bigbed_to_bigwig(bigbed_file_path, output_file_path,genome_dt):
    genome_file = open(genome_dt)
    chr_length_dt = {}
    for line in genome_file:
        line_list = line.strip().split("\t")
        chr_length_dt[line_list[0]] = int(line_list[1])
    genome_file.close()
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
    b.write(chr_length_dt, bigbed_to_bigwig(bigbed_file_path))

def main(bam_file_path,
         bw_filw_path,
         genome_dt,
         tmp_path="./test_random.bigbed",
         threads=1,
         binsize=10,
         verbose="INFO",
         scale_method="cpm"):
    """

    :param bam_file_path:
    :param bw_filw_path:
    :param tmp_path:
    :param binsize:
    :param verbose:
    :return:
    """
    # set_logging_level(verbose)
    FORMAT = "%(message)s"
    logging.basicConfig(
        level=verbose, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )

    log = logging.getLogger("rich")
    log.info("start calculation")
    #logging.info("start")
    console = Console()
    with console.status("[bold green]Working on tasks...") as status:
        convert_bam_to_bigbed(bam_file_path,tmp_path,genome_dt,thread=threads,binsize = binsize,scale_method=scale_method)
    log.info("start convert bigbed to bigwig")
    covert_bigbed_to_bigwig(tmp_path, bw_filw_path,genome_dt)
    import os
    os.remove(tmp_path)
    log.info("end")


if __name__ == "__main__":
    main("../data/293.ChIP.H3K36me3.rep1.ENCFF899GOH.bam",
         "../data/test.bw",
         genome_dt="../data/genome.fa.fai",
          tmp_path="../data/293.ChIP.H3K36me3.rep1.ENCFF899GOH.bedGraph",
         threads=16,
         scale_method="none")
    # logging.info("start count bam")
    # convert_bam_to_bigbed("../data/293.ChIP.H3K36me3.rep1.ENCFF899GOH.bam", "293.ChIP.H3K36me3.rep1.ENCFF899GOH.bedGraph")
    # logging.info("start convert bigbed to bw file")
    # covert_bigbed_to_bigwig("../data/293.ChIP.H3K36me3.rep1.ENCFF899GOH.bedGraph", "../data/293.ChIP.H3K36me3.rep1.ENCFF899GOH.bw")
    # logging.info("finish")
    # # for chr_name in chr_length_dt:
    # #     print(chr_name)
    # #     coverage = query_target_region_bin(bs_file, [(chr_name,0,chr_length_dt[chr_name])])
    # #     print(coverage)
    # start_time = time.time()
    # # 并行
    #
    # print("parallel")
    #
    # thread = 10
    # for chr_name in chr_length_dt:
    #     pool = Pool(processes=thread)
    #     #print(chr_name)
    #     chr_bins = int(chr_length_dt[chr_name] / 10)
    #     coverage_list = []
    #     for i in range(thread):
    #         coverage_list.append(pool.apply_async(query_target_region_bin, args=([chr_name,int(i*chr_bins/thread)*10,int((i+1)*chr_bins/thread)*10],)))
    #     #coverage_list.append(pool.apply_async(query_target_region_bin, args=([chr_name,0,chr_length_dt[chr_name]],)))
    #     # coverage = pool.apply_async(query_target_region_bin, args=(bs_file, [(chr_name,0,chr_length_dt[chr_name])]))
    #     # print(coverage)
    #     pool.close()
    #     pool.join()
    #     merge_total_count_list = []
    #     for temp_index, res in enumerate(coverage_list):
    #         run_res = res.get()
    #         # print(run_res)
    #         merge_total_count_list.append(run_res)
    #     f = open("../data/293.ChIP.H3K36me3.rep1.ENCFF899GOH.chr1.bedGraph", "w")
    #     for temp_index, res in enumerate(merge_total_count_list):
    #         # print(res)
    #         for temp_index, res in enumerate(res):
    #             # print(res)
    #             f.write(str(res[0]) + "\t" + str(res[1]) + "\t" + str(res[2]) + "\t" + str(res[3]) + "\n")
    #     print("time:", (time.time() - start_time)/60)
    #     f.close()
    # pool = Pool(processes=2)
    # coverage_list = []
    # for chr_name in chr_length_dt:
    #     print(chr_name)
    #     coverage_list.append(pool.apply_async(query_target_region_bin, args=(bs_file, [(chr_name,0,chr_length_dt[chr_name])])))
    # pool.close()
    # pool.join()
    # # for temp_index, res in enumerate(coverage_list):
    # #     run_res = res.get()
    # #     print(run_res)
