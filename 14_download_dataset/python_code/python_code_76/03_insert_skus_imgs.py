# INSERE DADOS DAS IMAGENS DE CADA SKU

# ======================================
exit(0)
# ======================================

from libs import *

mydb = mysql_connect('database_v')

table_skus = 'skus'
table_skus_imgs = 'skus_imgs'

sql = ' select * ' \
      ' from ' + table_skus + \
      ' order by id_sku;'
mycursor = mydb.cursor()
mycursor.execute(sql)
skus = mycursor.fetchall()

skus_num = len(skus)
skus_digits = len(str(skus_num))

count_skus_imgs = 0

print()
for sku in skus:

    for i in range(0, 6):

        id_img = str(count_skus_imgs + 1).rjust(9, '0')
        id_sku = str(sku[0]).rjust(9, '0')
        id_num = str(i + 1).rjust(2, '0')
        url = str.replace(sku[17+i], '"', "")
        ext = url.split(".")[-1]
        filename = id_img + '_' + id_sku + '_' + id_num + '.' + ext

        sql = ' insert into ' + table_skus_imgs + \
              ' (id_sku, id_num, url, name) ' \
              ' values (%s, %s, %s, %s);'

        values = (id_sku, id_num, '%s' % url, '%s' % filename)
        mycursor = mydb.cursor()
        mycursor.execute(sql, values)

        count_skus_imgs += 1

    if (sku[0] % 5000 == 0) or (sku[0] == skus_num):

        mydb.commit()

        print('[' + str(sku[0]).rjust(skus_digits, '0') + '/' + str(len(skus)) + '] - Insertion OK')

mydb.close()

print('\nfinished')
