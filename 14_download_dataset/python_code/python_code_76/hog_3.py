from libs import *
import numpy as np
from sklearn.neighbors import KDTree
import joblib

class_name = 'mocassim'
descriptors_dir = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/logs_hog/' + class_name + '/descriptors'
tree_dir = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/logs_hog/' + class_name + '/tree/KDTree.joblib'

#metric = 'euclidean'
#metric = 'manhattan'
#metric = 'chebyshev'
metric = 'minkowski'

imgs_paths = get_all_file_paths(descriptors_dir, '.out')
imgs_paths.sort()
imgs_paths_num = len(imgs_paths)

if imgs_paths_num == 0:
    print('No files founded, aborted.')
    exit(0)

descriptors_list = []
for img_path in imgs_paths:
    descriptor = np.loadtxt(img_path)
    descriptors_list.append(descriptor)
descriptors_list = np.asarray(descriptors_list, dtype=np.float)

tree = KDTree(descriptors_list, leaf_size=40, metric=metric)

joblib.dump(tree, tree_dir)
