# VERIFICA SE HÁ IMAGENS NO DIRETÓRIO QUE NÃO ESTÃO DADAS COMO BAIXADAS
# SE HOUVER, DELETA, POIS PROVAVELMENTE SÃO DOWNLOADS ABORTADOS, IMAGENS CORROMPIDAS OU COM PROBLEMAS

# ======================================
#exit(0)
# ======================================

import numpy as np
from libs import *

mydb = mysql_connect('database_v3')

directory = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/images/images_v3'
#directory='/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_1 (copy)'
#directory = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_2/nearest_skus_imgs_dups (copy)'
#directory='/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_1/filter_1_remove'
#directory='/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/filter_2/nearest_skus_imgs_dups (copy)_remove'

table_skus_imgs = 'skus_imgs'

imgs_paths = get_all_file_paths(directory, '.jpg')
imgs_paths.sort()
imgs_paths_num = len(imgs_paths)

if imgs_paths_num == 0:
    print('No files founded, aborted.')
    exit(0)

sql = ' select id_img ' \
      ' from ' + table_skus_imgs + \
      ' where download="Download file ok";'
mycursor = mydb.cursor()
mycursor.execute(sql)
imgs_database = np.array(mycursor.fetchall(), dtype=np.int)

count_imgs = 1
count_removed = 0

for img_path in imgs_paths:

    filename = os.path.basename(img_path)

    id_img = int(filename[0:9])

    result_search = bin_search(imgs_database[:, 0], id_img, 0, len(imgs_database) - 1)

    if result_search == -1:

        os.remove(img_path)

        print('[' + str(count_imgs) + '/' + str(imgs_paths_num) + '] - img removed: ' + img_path)

        count_removed += 1

    #else:
    #    pass
        #print('[' + str(count_imgs) + '/' + str(imgs_paths_num) + '] - img OK: ' + img_path)

    #exit(0)

    count_imgs += 1

print('\nimgs removed: ' + str(count_removed))

mydb.close()
