from libs import *
from glob import glob
import os
import shutil

directory_1 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_1 (copy)/nearest_skus_imgs_dups_1'
directory_2 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_1/nearest_skus_imgs_dups_3'
#directory_2 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/tree_nearest_skus_imgs'

#directory_1 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_2/nearest_skus_imgs_dups (copy)'
#directory_2 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_2/nearest_skus_imgs_dups'
#directory_2 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_2/nearest_skus_imgs_all'

aux = glob(directory_1 + '/*')
aux.sort()

folders = []
for x in aux:
    folders.append(os.path.basename(x))

folder_prior = ''
count = 0

folders_not = []

for folder in folders:

    filenames_01 = os.listdir(directory_1 + slash + folder)
    filenames_01.sort()

    if os.path.isdir(directory_2 + slash + folder):

        filenames_02 = os.listdir(directory_2 + slash + folder)
        filenames_02.sort()

        if len(filenames_01) < len(filenames_02):
            print(str(len(filenames_01)) + ' ' + str(len(filenames_02)) + ' - ' + folder)
