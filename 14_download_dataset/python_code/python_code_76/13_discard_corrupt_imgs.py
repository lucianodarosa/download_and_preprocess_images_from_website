# REMOVE TODAS AS IMAGENS IDENTIFICADAS COMO CORROMPIDAS
# EM PELOMENOS UMA DAS TRÊS ETAPAS DE CHECAGEM
# OBS: (REMOVE DA PASTA E ATUALIZA O STATUS DE DOWNLOAD NO DATABASE)

# ======================================
exit(0)
# ======================================

import numpy as np
from libs import *

mydb = mysql_connect('database_v2')

table_skus_imgs = 'skus_imgs'


def find_skus_imgs_corrupted():

    sql = ' select id_img, id_sku, id_num, url, name, path '\
          ' from ' + table_skus_imgs + \
          ' where download = "Download file ok" '\
          ' and (check_1=1 or check_2=1 or check_3=1);'
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    skus_images = np.array(mycursor.fetchall(), dtype=str)
    return skus_images


skus_imgs = find_skus_imgs_corrupted()
skus_imgs_num = len(skus_imgs)
skus_imgs_digits = len(str(skus_imgs_num))

count_removed = 0

print()
for sku_img in skus_imgs:

    id_img = sku_img[0]
    name = sku_img[4]
    path = sku_img[5]

    os.remove(path + slash + name)

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
    #'''

    print('file removed: ' + path + slash + name)

    count_removed +=1

print('\nimgs removed: ' + str(count_removed))

mydb.close()
