from libs import *
from glob import glob
import os
import shutil

directory_1 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_2/nearest_skus_imgs_dups (copy)'
directory_2 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_2/nearest_skus_imgs_all'
directory_3 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/logs_hash'

aux = glob(directory_1 + '/*')
aux.sort()

folders = []
for x in aux:
    folders.append(os.path.basename(x))

count = 0

folders_not = []

for folder in folders:

    if os.path.isdir(directory_2 + slash + folder):

        filenames = os.listdir(directory_2 + slash + folder)
        filenames.sort()

        for filename in filenames:

            ext = os.path.splitext(filename)[1]
            name = str.replace(filename, ext, '')
            path = directory_1 + slash + folder + slash + name + ext
            path_old = directory_2 + slash + folder + slash + name + ext

            if not os.path.isfile(path):
                shutil.copy(path_old, path)

        count += 1

    else:
        folders_not.append(folder)


print('\n'+str(count)+'\n')

for folder_not in folders_not:
    if os.path.isdir(directory_3 + slash + folder_not):
        print(folder_not)

print()

for folder_not in folders_not:
    if not os.path.isdir(directory_3 + slash + folder_not):
        print(folder_not)
