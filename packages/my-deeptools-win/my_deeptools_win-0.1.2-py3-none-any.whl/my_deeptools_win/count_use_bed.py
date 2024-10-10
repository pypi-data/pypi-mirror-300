import logging

from my_deeptools_win._counter import multi_region_file_BAM_count
from my_deeptools_win.__logging import set_logging_level
from my_deeptools_win._spliter import  split_file_and_make_temp
def main(input,
            bams: str,
            tags,
            output: str=None,
            method: str="CPM",
            process: int =1,
            mapq: int = 20,
            strand: str = "b",
            extend_length : int = 1,
            temp_dir: str = None,
            verbose: str = "INFO",):
    set_logging_level(verbose)
    bam_file_list = bams.split(",") if not isinstance(bams, tuple) else list(bams)
    bam_tags_list = tags.split(",") if not isinstance(tags, tuple) else list(tags)
    assert len(bam_file_list) == len(bam_tags_list), "bam file list and tags list should have same length"
    print(bam_file_list)
    print(bam_tags_list)
    # split bed file

    region_split_filename_list = split_file_and_make_temp(input_file_name = input,
                                                           n_part = process,
                                                           temp_dir = temp_dir)
    #logging.info("split bed file")
    # count file

    final_count_dict = {}
    tag_res_list = []

    for bam_index, run_bam_filename in enumerate(bam_file_list):
        bam_tag = bam_tags_list[bam_index]
        count_list = multi_region_file_BAM_count(
            region_filename_list=region_split_filename_list,
            bam_filename=run_bam_filename,
            thread_num=process,
            MAPQ_cutoff=mapq,
            strand_select_method=strand,
            extend_length=extend_length,
            norm_method=method
        )
        # dict_key = "%s_%s" % (bam_tag,bam_index)
        # final_count_dict[dict_key] = count_list
        # tag_res_list.append(dict_key)
        
if __name__ == '__main__':
    main(1,2)