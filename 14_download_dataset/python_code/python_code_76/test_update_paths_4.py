from libs import *
from glob import glob
import os
import shutil

directory_1 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_1 (copy)/nearest_skus_imgs_dups_1'
#directory_1 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_2/nearest_skus_imgs_dups (copy)'

directory_2 = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/logs_hash'

aux = glob(directory_1 + '/*')
aux.sort()

folders = []
for x in aux:
    folders.append(os.path.basename(x))

folder_prior = ''
count = 0

for folder in folders:

    if os.path.isdir(directory_2 + slash + folder):

        print(folder)
