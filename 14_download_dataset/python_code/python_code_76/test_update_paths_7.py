from libs import *
from glob import glob
import os
import shutil

#directory_1 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_1/filter_1 (copy)/nearest_skus_imgs_dups_1'
#directory_2 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_1/filter_1_remove'

directory_1 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_2/nearest_skus_imgs_dups (copy)'
directory_2 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_2/nearest_skus_imgs_dups (copy)_remove'

aux = glob(directory_1 + '/*')
aux.sort()

folders = []
for x in aux:
    folders.append(os.path.basename(x))

count = 0

for folder in folders:

    filenames = os.listdir(directory_1 + slash + folder)
    filenames.sort()

    for filename in filenames[1:]:

        ext = os.path.splitext(filename)[1]
        name = str.replace(filename, ext, '')
        path_2 = directory_2 + slash + name + ext
        path_old = directory_1 + slash + folder + slash + name + ext

        if not os.path.isfile(path_2):
            shutil.copy(path_old, path_2)
            print('copy - ' + path_2)
            count += 1

print('\n'+str(count)+'\n')
