# VERIFICA SE AS IMAGENS QUE ESTÃO DADAS COMO BAIXADAS REALMENTE ESTÃO NO DIRETÓRIO
# SE NÃO ESTIVEREM, ATUALIZA O STATUS DE DOWNLOAD PARA NULL

# ======================================
#exit(0)
# ======================================

import numpy as np
from libs import *

mydb = mysql_connect('database_v3')

directory = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/images/images_v3/'
table_skus_imgs = 'skus_imgs'

imgs_paths = get_all_file_paths(directory, '.jpg')
imgs_paths.sort()
imgs_paths_num = len(imgs_paths)

if imgs_paths_num == 0:
    print('No files founded, aborted.')
    exit(0)

imgs_paths_ids = []
for img_path in imgs_paths:
    imgs_paths_ids.append(int(os.path.basename(img_path)[0:9]))
imgs_paths_ids = np.array(imgs_paths_ids, dtype=np.int)
imgs_paths_ids = np.sort(imgs_paths_ids)
imgs_paths_ids_num = len(imgs_paths_ids)

sql = ' select id_img, id_sku, id_num, name ' \
      ' from ' + table_skus_imgs + \
      ' where download = "Download file ok";'
mycursor = mydb.cursor()
mycursor.execute(sql)
imgs_database = np.array(mycursor.fetchall(), dtype=str)

count_updates = 0
count_imgs = 0

for img_database in imgs_database:

    id_img = int(img_database[0])
    filename = str(img_database[3])

    result_search = bin_search(imgs_paths_ids, id_img, 0, len(imgs_paths_ids) - 1)

    if result_search == -1:

        print('[' + str(count_imgs) + '/' + str(imgs_paths_ids_num) + '] - img not finded: ' + filename)

        #'''
        sql = ' update ' + table_skus_imgs + ' set '\
              ' download=null, '\
              ' check_1=null, '\
              ' check_2=null '\
              ' where id_img=' + str(id_img) + ';'
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
        #'''

        count_updates += 1

    else:
        continue
        print('[' + str(count_imgs) + '/' + str(imgs_paths_ids_num) + '] - img finded: ' + filename)

    count_imgs += 1

print('\nimgs updated: ' + str(count_updates))

mydb.close()
