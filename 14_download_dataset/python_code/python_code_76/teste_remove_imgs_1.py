# ======================================
#exit(0)
# ======================================

import numpy as np
from libs import *


class_name = 'mocassim'
directory_1 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/Untitled Folder/calcados/' + class_name + '_remove'
directory_2 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/logs_hog/' + class_name + '/neighbors'

imgs_paths_1 = get_all_file_paths(directory_1, '.jpg')
imgs_paths_1.sort()
imgs_paths_1 = np.array(imgs_paths_1, dtype=str)
imgs_paths_1 = np.unique(imgs_paths_1)
imgs_paths_1_num = len(imgs_paths_1)
imgs_paths_1_digits = len(str(imgs_paths_1_num))

imgs_paths_2 = get_all_file_paths(directory_2, '.jpg')
imgs_paths_2.sort()
imgs_paths_2 = np.array(imgs_paths_2, dtype=str)
imgs_paths_2_num = len(imgs_paths_2)
imgs_paths_2_digits = len(str(imgs_paths_2_num))

if imgs_paths_1_num == 0 or imgs_paths_2_num == 0:
    print('No files founded, aborted.')
    exit(0)

count_removed = 0

print()
for img_path_1 in imgs_paths_1:

    name = os.path.basename(img_path_1)[5:]
    id_img_1 = int(name[0:9])

    for i, img_path_2 in enumerate(imgs_paths_2):

        name = os.path.basename(img_path_2)[5:]
        id_img_2 = int(name[0:9])

        if id_img_1 == id_img_2:

            try:
                os.remove(img_path_2)
                print('file removed: ' + str(img_path_2))
                count_removed += 1
                np.delete(img_path_2, i)
            except:
                pass

print('\nimgs removed: ' + str(count_removed))
