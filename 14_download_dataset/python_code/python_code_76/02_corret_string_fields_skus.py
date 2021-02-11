# CORRIGE CAMPOS NULL DOS SKUS

# ======================================
exit(0)
# ======================================

from libs import *

table_skus = 'skus'

mydb = mysql_connect('database_v1')

mycursor = mydb.cursor()

fields = ['sku_config', 'product_name', 'product_description', 'cat_1', 'cat_2', 'cat_3', 'cat_4', 'cat_5', 'cat_6',
          'main_category', 'sub_category', 'gender', 'brand', 'sizes_available', 'store', 'is_marketplace',
          'aditional_image_url_1', 'aditional_image_url_2', 'aditional_image_url_3', 'aditional_image_url_4',
          'aditional_image_url_5', 'aditional_image_url_6', 'google_product_category']

print()
for field in fields:

    sql = ' update ' + table_skus + ' set ' \
          ' ' + field + ' =null ' \
          ' where ' + field + ' = "nan";'

    mycursor.execute(sql)
    mydb.commit()

    print(field + ' - update OK')

mydb.close()

print('\nfinished')
