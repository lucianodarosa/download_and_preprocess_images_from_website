# REMOVE IMAGENS COM CÓDIGOS HASH IGUAIS
# PERMANECENDO APENAS A PRIMEIRA OCORRÊNCIA

# ======================================
exit(0)
# ======================================

import numpy as np
import shutil
from libs import *

mydb = mysql_connect('database_v2')

path_out = './dup_hashes'
table_skus_imgs = 'skus_imgs'


def find_skus_imgs():

    _sql = ' select id_img, path, name, hash '\
           ' from ' + table_skus_imgs + \
           ' where download = "Download file ok" '\
           ' and hash is not null '\
           ' order by hash, id_img, id_sku, id_num;'#\
           #' limit 5000;'
    mycursor = mydb.cursor()
    mycursor.execute(_sql)
    _skus_images = np.array(mycursor.fetchall(), dtype=str)
    return _skus_images


def find_hashes():

    _sql = ' select hash ' \
           ' from ' + table_skus_imgs + \
           ' where download = "Download file ok" '\
           ' and hash is not null' \
           ' order by hash, id_img, id_sku, id_num;'#\
           #' limit 5000;'
    mycursor = mydb.cursor()
    mycursor.execute(_sql)
    _hashes = np.array(mycursor.fetchall(), dtype=str)
    return _hashes


skus_imgs = find_skus_imgs()
hashes = find_hashes()

_, ids_un, counts_un = np.unique(hashes[:, 0], return_index=True, return_counts=True)

values_dup, ids_dup, counts_dup = [], [], []
for i in range(len(counts_un)):

    if counts_un[i] >= 2:

        ids_dup.append(ids_un[i])
        counts_dup.append(counts_un[i])

ids_dup = np.asarray(ids_dup, dtype=np.int)
counts_dup = np.asarray(counts_dup, dtype=np.int)

if len(ids_dup) == 0:
    print('No duplicate founded!')
    exit(0)

count_folder = 0

for i in range(len(skus_imgs)):

    if skus_imgs[i][3] != hash:

        id_unique = bin_search(ids_dup, i, 0, len(ids_dup) - 1)

        if id_unique != -1:

            id_count = counts_dup[id_unique]

            if id_count > 1:

                print('============ ' + skus_imgs[i][2])

                hash = skus_imgs[i][3]

                _name_quote, _ext_in = os.path.splitext(skus_imgs[i][2])

                #print(_name_quote)
                #exit(0)

                #folder_name = 'dups_' + str(count_folder + 1)
                folder_name = str(_name_quote)
                os.mkdir(path_out + slash + folder_name)
                count_folder += 1

                shutil.copy(skus_imgs[i][1] + slash + skus_imgs[i][2], path_out + slash + folder_name + slash + skus_imgs[i][2])
    else:

        print(skus_imgs[i][2])

        shutil.copy(skus_imgs[i][1] + slash + skus_imgs[i][2], path_out + slash + folder_name + slash + skus_imgs[i][2])

        #'''
        os.remove(skus_imgs[i][1] + slash + skus_imgs[i][2])
        
        sql = ' update ' + table_skus_imgs + ' set ' \
              ' path=null, ' \
              ' download="Duplicate file hash", ' \
              ' check_1=null, '\
              ' check_2=null, ' \
              ' check_3=null, ' \
              ' hash=null ' \
              ' where id_img=' + skus_imgs[i][0] + ';'
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
        #'''
