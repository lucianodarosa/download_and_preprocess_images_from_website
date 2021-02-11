from libs import *
from glob import glob
import os
import shutil

#directory_1 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_1 (copy)/nearest_skus_imgs_dups_3'
#directory_2 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_1_/nearest_skus_imgs_dups_3'

directory_1 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_2/nearest_skus_imgs_dups (copy)'
directory_2 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_2/nearest_skus_imgs_dups'

aux = glob(directory_2 + '/*')
aux.sort()

folders = []
for x in aux:
    folders.append(os.path.basename(x))

folder_prior = ''
count = 0

for folder in folders:

    if not os.path.isdir(directory_1 + slash + folder):

        print(folder)
