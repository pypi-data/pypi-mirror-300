import os
import logging
import random
import string
import gzip


def split_file_and_make_temp(input_file_name,
                             n_part = 1,
                             temp_dir=None):
    if temp_dir:
        temp_dir = os.path.abspath(temp_dir)
    else:
        temp_dir = os.path.dirname(input_file_name)

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        logging.info(f"Create temp dir: {temp_dir}")
    input_file_basename = os.path.basename(input_file_name)

    logging.info(f"Split file: {input_file_basename}")
    temp_file_list = []
    temp_filename_list = []

    for index in range(n_part):
        rnd_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        temp_file_basename = f"temp_{input_file_basename}.{index}.{rnd_str}"
        #print(temp_file_basename)
        #logging.info(f"Create temp file: {temp_file_basename}")
        temp_file_name = os.path.join(temp_dir, temp_file_basename)
        temp_filename_list.append(temp_file_name)

        temp_file_list.append(open(temp_file_name,"wt"))

    logging.info("Counting input file")

    total_input_line_num = 0
    input_file = open(input_file_name,"rt") if not input_file_name.endswith(".gz") else gzip.open(input_file_name,"rt")
    for line in input_file:
        #print(line)
        total_input_line_num += 1
    input_file.close()
    # print(f"Total input line num: {total_input_line_num}")
    if total_input_line_num % n_part == 0:
        each_file_line_num = total_input_line_num // n_part
    else:
        each_file_line_num = total_input_line_num // n_part + 1

    logging.info("Start to split")

    input_file = open(input_file_name,"rt") if not input_file_name.endswith(".gz") else gzip.open(input_file_name,"rt")
    for index, line in enumerate(input_file):
        file_index = index // each_file_line_num
        temp_file_list[file_index].write(line)
    input_file.close()
    for temp_file in temp_file_list:
        temp_file.close()

    logging.info("Split done")
    return temp_filename_list
