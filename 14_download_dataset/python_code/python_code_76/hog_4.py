# EXECUTA A BUSCA PELOS VIZINHOS MAIS PRÓXIMOS
# RECUPERA VIZINHOS COM ÍNDICE DE SEMELHANÇA <= 0.1
# SALVA A QUERY E OS RESULTADOS EM UMA PASTA PARA CONFERÊNCIA

# ======================================
#exit(0)
# ======================================

import numpy as np
import shutil
import joblib
from libs import *

class_name = 'mocassim'
imgs_dir = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/Untitled Folder/calcados/' + class_name
queries_path = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/logs_hog/' + class_name + '/queries'
descriptors_dir = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/logs_hog/' + class_name + '/descriptors'
tree_dir = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/logs_hog/' + class_name + '/tree/KDTree.joblib'
k_neighbors_dir = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/logs_hog/' + class_name + '/neighbors'
k_neighbors = 500


def find_nn(_img_query):

    filename = os.path.basename(_img_query)
    ext = os.path.splitext(filename)[1]
    name = str.replace(filename, ext, '')

    _id_query = np.where(imgs_paths == imgs_dir + slash + filename)[0][0]

    dist, ind = tree.query(dp_list[_id_query:_id_query + 1], k=k_neighbors)

    new_folder_name = k_neighbors_dir + slash + name
    os.mkdir(new_folder_name)

    count = 0

    shutil.copy(imgs_dir + slash + filename, new_folder_name + slash + str(str(count)).rjust(4, '0') + '_' + filename)

    for i in ind[0]:

        filename = os.path.basename(imgs_paths[i])
        shutil.copy(imgs_dir + slash + filename, new_folder_name + slash + str(str(count)).rjust(4, '0') + '_' + filename)
        count += 1


imgs_paths = get_all_file_paths(imgs_dir, '.jpg')
imgs_paths.sort()
imgs_paths = np.array(imgs_paths, dtype=np.str)
imgs_paths_num = len(imgs_paths)

dp_paths = get_all_file_paths(descriptors_dir, '.out')
dp_paths.sort()
dp_paths_num = len(dp_paths)

queries_paths = get_all_file_paths(queries_path, '.jpg')
queries_paths.sort()
queries_paths_num = len(queries_paths)

if dp_paths_num == 0 or imgs_paths_num == 0 or queries_paths_num == 0:
    print('No files founded, aborted.')
    exit(0)

dp_list = []
for dp_path in dp_paths:
    dp = np.loadtxt(dp_path)
    dp_list.append(dp)
dp_list = np.asarray(dp_list, dtype=np.float)

tree = joblib.load(tree_dir)

for queries_path in queries_paths:

    try:
        find_nn(queries_path)
    except:
        continue
