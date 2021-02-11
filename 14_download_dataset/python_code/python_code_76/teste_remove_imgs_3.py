# ======================================
#exit(0)
# ======================================

import numpy as np
from libs import *

class_name = 'mocassim'
directory_1 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/Untitled Folder/calcados/' + class_name + '_remove'
directory_2 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/Untitled Folder/calcados/' + class_name

imgs_paths = get_all_file_paths(directory_1, '.jpg')
imgs_paths.sort()
imgs_paths = np.array(imgs_paths, dtype=str)
imgs_paths_num = len(imgs_paths)
imgs_paths_digits = len(str(imgs_paths_num))

if imgs_paths_num == 0:
    print('No files founded, aborted.')
    exit(0)

count_removed = 0

print()
for img_path in imgs_paths:

    if os.path.basename(img_path)[4:5] == '_':
        name = os.path.basename(img_path)[5:]
    else:
        name = os.path.basename(img_path)

    id_img = int(name[0:9])

    _id_aux = np.where(imgs_paths == img_path)[0][0]
    _progress = '[' + str(_id_aux + 1).rjust(imgs_paths_digits, '0') + '/' + str(imgs_paths_num) + '] - '

    try:
        os.remove(directory_2 + slash + name)
    except:
        continue

    print(_progress + 'file removed: ' + str(directory_2) + slash + str(name))

    count_removed += 1

print('\nimgs removed: ' + str(count_removed))
