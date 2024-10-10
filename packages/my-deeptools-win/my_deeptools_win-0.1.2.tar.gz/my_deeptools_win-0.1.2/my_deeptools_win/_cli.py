from fire import Fire
from my_deeptools_win.count_use_bed import main as run_count_use_bed
from my_deeptools_win.multi_test import  main as convert_bam_to_bw
class Cli(object):
    """Cli interface of python package <deep_tools>

    """
    def count_use_bed(
            self,
            input,
            bams: str,
            tags,
            output: str=None,
            method: str="CPM",
            process: int =1,
            mapq: int = 20,
            strand: str = "b",
            extend_length : int = 1,
            temp_dir: str = None,
            verbose: str = "ERROR",
        ):
        """

        :param input:
        :param bams:
        :param output:
        :param method:
        :param process:
        :param mapq:
        :param strand:
        :param extend_length:
        :param temp_dir:
        :param verbose:
        :return:
        """
        return run_count_use_bed(
            input = input,
            bams = bams,
            output = output,
            tags = tags,
            method = method,
            process = process,
            mapq = mapq,
            strand = strand,
            extend_length = extend_length,
            temp_dir = temp_dir,
            verbose = verbose
        )
    def bamcovrrage(self,
                    bam_file_path,
                    bw_filw_path,
                    genome_dt,
                    threads=1,
                    binsize=10,
                    verbose="INFO",
                    tmp_path="./test_random.bigbed",
                    scale_method="cpm"
                    ):
        """
        convert bam file to bigwig file,
        :param bam_file_path: bam file path
        :param bw_file_path: out put bigwig file path
        :param genome_dt: genome length file ,such as .fai file
        :param threads: threads number
        :param binsize: genome binsize
        :param verbose:
        :param tmp_path: tmp bigbed file path
        :param scale_method: scale method function include rpkm ,cpm and none
        :return:
        """
        return convert_bam_to_bw(
            bam_file_path,
            bw_filw_path,
            genome_dt,
            threads=threads,
            binsize=binsize,
            verbose=verbose,
            tmp_path = tmp_path,
            scale_method=scale_method
        )

def main():
    cli = Cli()
    Fire(cli, name='my_deeptools_win')

if __name__ == '__main__':
    main()