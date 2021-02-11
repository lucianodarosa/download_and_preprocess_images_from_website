# SEPARA AS IMAGENS EM PASTAS PARA FACILITAR O MANUSEIO E VISUALIZAÇÃO

# ======================================
exit(0)
# ======================================

import shutil
from libs import *

path_in = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/images/images_v1/'
path_out = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/images/images_v2/'

files = get_all_file_paths(path_in, '.jpg')
files.sort()
files_num = len(files)

if files_num == 0:
    print('No files founded, aborted.')
    exit(0)

split_size = 5000
split_num = get_shard_num(files_num, split_size)
split_digits = len(str(split_num))
split_count = 1
row_split_count = 1
row_count = 0

id_img_ini = int(os.path.basename(files[0])[0:9])
id_img_end = 0

for file in files:

    filename = os.path.basename(file)

    if row_count % split_size == 0:

        new_folder_name = 'split_' + str(split_count).rjust(split_digits, '0')

        os.mkdir(path_out + new_folder_name)

    shutil.copy(file, path_out + new_folder_name + '/' + filename)

    if row_split_count == split_size or row_count + 1 == files_num:

        id_img_end = int(filename[0:9])

        print('split: ' + str(split_count).rjust(split_digits, '0') + '/' + str(split_num) + ' - [' + str(
            id_img_ini) + ' - ' + str(id_img_end) + ']')

        try:
            id_img_ini = int(os.path.basename(files[row_count + 1])[0:9])
        except:
            pass

        row_split_count = 1
        split_count += 1

    else:
        row_split_count += 1

    row_count += 1
