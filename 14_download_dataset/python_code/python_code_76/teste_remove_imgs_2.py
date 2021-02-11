# ======================================
#exit(0)
# ======================================

import numpy as np
from libs import *

mydb = mysql_connect('database_v3')

directory = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/Untitled Folder/acessorios/cat_1/relogio_remove'

table_skus_imgs = 'skus_imgs'

imgs_paths = get_all_file_paths(directory, '.jpg')
imgs_paths.sort()
imgs_paths = np.array(imgs_paths, dtype=str)
imgs_paths_num = len(imgs_paths)
imgs_paths_digits = len(str(imgs_paths_num))

if imgs_paths_num == 0:
    print('No files founded, aborted.')
    exit(0)

count_removed = 0

print()
for img_path in imgs_paths:

    name = os.path.basename(img_path)[5:]

    id_img = int(name[0:9])

    try:

        _sql = ' select path, name ' + \
               ' from ' + table_skus_imgs + \
               ' where download = "Download file ok" ' \
               ' and id_img=' + str(id_img) + ';'
        mycursor = mydb.cursor()
        mycursor.execute(_sql)
        path = mycursor.fetchone()[0]

    except:
        continue

    if path != None:

        _id_aux = np.where(imgs_paths == img_path)[0][0]
        _progress = '[' + str(_id_aux + 1).rjust(imgs_paths_digits, '0') + '/' + str(imgs_paths_num) + '] - '

        # '''
        try:
            os.remove(path + slash + name)
        except:
            pass

        sql = ' update ' + table_skus_imgs + ' set ' \
              ' path=NULL, ' \
              ' download="Discarded file", ' \
              ' check_1=NULL, ' \
              ' check_2=NULL, ' \
              ' check_3=NULL ' \
              ' where id_img=' + str(id_img) + ';'
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
        # '''

        print(_progress + 'file removed: ' + str(path) + slash + str(name))

        count_removed += 1

print('\nimgs removed: ' + str(count_removed))

mydb.close()
