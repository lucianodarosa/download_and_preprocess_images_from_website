# REMOVE SKUS COM IMAGENS IGUAIS

# ======================================
exit(0)
# ======================================

import numpy as np
from libs import *

mydb = mysql_connect('database_v1')

table_skus = 'skus'
table_skus_imgs = 'skus_imgs'

sql = ' select url, id_sku '\
      ' from ' + table_skus_imgs + \
      ' where id_num = 1 '\
      ' order by url, id_sku;'

mycursor = mydb.cursor()
mycursor.execute(sql)
skus_images = np.array(mycursor.fetchall(), dtype=str)

skus = []
url_prior = skus_images[0][0]

for sku_image in skus_images[1:]:

    if str(url_prior) == str(sku_image[0]):
        skus.append(sku_image[1])
    else:
        url_prior = sku_image[0]

skus_num = len(skus)
skus_digits = len(str(skus_num))

count_skus = 1



print()
for sku in skus:

    '''
    sql = ' delete from ' + table_skus + \
          ' where id_sku = ' + str(sku) + ';'
    mycursor.execute(sql)
    '''

    if (count_skus % 5000 == 0) or (count_skus == skus_num):

        #mydb.commit()

        print('[' + str(count_skus).rjust(skus_digits, '0') + '/' + str(skus_num) + '] - deleted skus OK')

    count_skus += 1

mydb.close()

print('\nfinished')
