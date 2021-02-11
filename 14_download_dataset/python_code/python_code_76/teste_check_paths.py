from libs import *
import numpy as np
import os

directory = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/tree_nearest_skus_imgs'

skus_imgs = get_all_file_paths(directory, '.jpg')
skus_imgs.sort()
skus_imgs = np.array(skus_imgs, dtype=str)
skus_imgs_num = len(skus_imgs)
skus_imgs_digits = len(str(skus_imgs_num))


print(os.path.basename(os.path.dirname(skus_imgs[0])))
exit(0)



paths = ([x[0] for x in os.walk(directory)])

print()

print(paths[0])
print(paths[1])
print(paths[2])
print(paths[3])
print(paths[4])

print()

print(os.path.basename(os.path.dirname(paths[0])))
print(os.path.basename(os.path.dirname(paths[1])))
print(os.path.basename(os.path.dirname(paths[2])))
print(os.path.basename(os.path.dirname(paths[3])))
print(os.path.basename(os.path.dirname(paths[4])))

print()
