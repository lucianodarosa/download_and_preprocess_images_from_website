from libs import *
import numpy as np
import os

#directory = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/tree_nearest_skus_imgs'
directory = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_2/nearest_skus_imgs'
name_value = '1.jpg'

skus_imgs = get_all_file_paths(directory, '.jpg')
skus_imgs.sort()
skus_imgs = np.array(skus_imgs, dtype=str)
skus_imgs_num = len(skus_imgs)
skus_imgs_digits = len(str(skus_imgs_num))

for sku_img in skus_imgs:

    name_old = os.path.basename(sku_img)

    if name_old == name_value:

        folder = os.path.basename(os.path.dirname(sku_img))
        path = str.replace(sku_img, (slash + folder + slash + name_old), '')
        new = path + slash + folder + slash + folder + '.jpg'

        os.rename(sku_img, new)
