import logging
from multiprocessing import Pool
import bamnostic as bs
import os

def get_BAM_total_align_count(bam_filename):
    """
    INPUT:
        <bam_filename>
            BAM file path with .bai index file in a same dir

    RETURN
        <total_align_count>
            int, BAM file total align count

    """
    bam_file = bs.AlignmentFile(bam_filename, "rb")
    #bam_file.ge
    total_align_count = 0

    for bam_index_info in bam_file.get_index_stats():
        # ref_name = bam_index_info[0]
        map_count = bam_index_info[0]

        total_align_count += map_count

    bam_file.close()

    return total_align_count

def query_region_align_count(
        bam_obj,
        region_chr,
        region_start,
        region_end,
        strand_info=".",
        MAPQ_cutoff=20,
        strand_select_method="b",
        extend_length=1):
    query_align_count = 0

    for align in bam_obj.fetch(contig=region_chr,
                               start=region_start - extend_length,
                               end=region_end + extend_length):

        if align.mapq < MAPQ_cutoff:
            continue

        if strand_select_method == "s":
            if align.is_reverse and strand_info == "+":
                continue

            if not align.is_reverse and strand_info == "-":
                continue

        elif strand_select_method == "f":
            if align.is_reverse:
                continue

        elif strand_select_method == "r":
            if not align.is_reverse:
                continue

        elif strand_select_method == "b":
            pass

        else:
            raise ValueError("<strand_select_method> should be s, f, r or b!")

        query_align_count += 1

    return query_align_count

def region_file_BAM_count(
        region_filename,
        bam_filename,
        MAPQ_cutoff=20,
        strand_select_method="b",
        extend_length=1,
        norm_method="CPM"
):
    region_base_filename = os.path.basename(region_filename)
    bam_base_filename = os.path.basename(bam_filename)
    scale_factor = 1.0

    if norm_method == "CPM" or norm_method == "RPKM":
        bam_total_align_count = get_BAM_total_align_count(bam_filename)
        scale_factor = bam_total_align_count / 1e6
    print(bam_total_align_count)
    region_file = open(region_filename,"r")
    bam_file = bs.AlignmentFile(bam_filename,"rb")

    region_count_list = []
    for index,line in enumerate(region_file):
        if index % 1000 == 0:
            logging.info("Processed %d regions" % index)

        line_list = line.strip().split("\t")
        query_chr_name = line_list[0]
        query_start = int(line_list[1])
        query_end = int(line_list[2])

        if line_list[5] in ["+", "-","."]:
            query_strand_info = line_list[5]
        else:
            query_strand_info = "."

        query_count = query_region_align_count(
            bam_obj=bam_file,
            region_chr=query_chr_name,
            region_start=query_start,
            region_end=query_end,
            strand_info=query_strand_info,
            MAPQ_cutoff=MAPQ_cutoff,
            strand_select_method=strand_select_method,
            extend_length=extend_length
        )
        region_count_list.append(query_count * scale_factor)
    bam_file.close()
    region_file.close()
    return region_count_list
def multi_region_file_BAM_count(
        region_filename_list,
        bam_filename,
        thread_num=1,
        MAPQ_cutoff=20,
        strand_select_method="b",
        extend_length=1,
        norm_method="CPM"):
    logging.info("Starting multi_region_file_BAM_count")
    pool = Pool(processes=thread_num)

    input_BAM_count_result = []
    for query_region_filename in region_filename_list:
        input_BAM_count_result.append(
            pool.apply_async(region_file_BAM_count,
                             args=(query_region_filename,
                                   bam_filename,
                                   MAPQ_cutoff,
                                   strand_select_method,
                                   extend_length,
                                   norm_method))
        )
    pool.close()
    pool.join()

    merge_total_count_list = []
    for temp_index,res in enumerate(input_BAM_count_result):
        run_res = res.get()
        print(run_res)
        merge_total_count_list += run_res

    logging.info("Finished multi_region_file_BAM_count")
    print(merge_total_count_list)
    return merge_total_count_list