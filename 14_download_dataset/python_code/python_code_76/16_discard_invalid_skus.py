# REMOVE TODOS OS SKUS QUE NÃO POSSUEM IMAGENS VÁLIDAS

# ======================================
#exit(0)
# ======================================

import numpy as np
from libs import *

mydb = mysql_connect('database_v3')

table_skus = 'skus'
table_skus_imgs = 'skus_imgs'


def find_invalid_skus():

    _sql = ' select distinct(id_sku) '\
           ' from ' + table_skus_imgs + ' '\
           ' where download <> "Download file ok" '\
           ' group by id_sku '\
           ' having count(id_sku) = 6;'
    mycursor = mydb.cursor()
    mycursor.execute(_sql)
    _skus_images = np.array(mycursor.fetchall(), dtype=str)
    return _skus_images


skus_imgs = find_invalid_skus()
skus_imgs_num = len(skus_imgs)
skus_imgs_digits = len(str(skus_imgs_num))

count_removed = 0

print()
for sku_img in skus_imgs:

    id_sku = int(sku_img[0])

    sql = ' delete from ' + table_skus +\
          ' where id_sku=' + str(id_sku) + ';'
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()

    print('discarded sku: ' + str(id_sku))

    count_removed += 1

print('\nskus discarded: ' + str(count_removed))

mydb.close()
