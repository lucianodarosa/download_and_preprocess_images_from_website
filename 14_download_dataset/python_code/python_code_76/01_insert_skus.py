# INSERE OS DADOS NA TABELA SKUS

# ======================================
exit(0)
# ======================================

import pandas as pd
from libs import *

table_skus = 'skus'

dataset_path = '../../database/data.h5'

mydb = mysql_connect('database_v1')

mycursor = mydb.cursor()


def h5load(store):
 data = store['mydata']
 metadata = store.get_storer('mydata').attrs.metadata
 return data, metadata

with pd.HDFStore(dataset_path) as store:
    data, metadata = h5load(store)

data_num = len(data)
data_digits = len(str(data_num))

print()
for i, row in data.iterrows():

    sql = ' insert into ' + table_skus + \
          ' (sku_config, product_name, product_description, cat_1, cat_2, ' \
          ' cat_3, cat_4, cat_5, cat_6, main_category, sub_category, gender, ' \
          ' brand, sizes_available, store, is_marketplace, aditional_image_url_1, ' \
          ' aditional_image_url_2, aditional_image_url_3, aditional_image_url_4, ' \
          ' aditional_image_url_5, aditional_image_url_6, google_product_category) ' \
          ' values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'

    values = ('%s' % row['sku_config'],
              '%s' % row['product_name'],
              '%s' % row['product_description'],
              '%s' % row['cat_1'],
              '%s' % row['cat_2'],
              '%s' % row['cat_3'],
              '%s' % row['cat_4'],
              '%s' % row['cat_5'],
              '%s' % row['cat_6'],
              '%s' % row['main_category'],
              '%s' % row['sub_category'],
              '%s' % row['gender'],
              '%s' % row['brand'],
              '%s' % row['sizes_available'],
              '%s' % row['store'],
              '%s' % row['is_marketplace'],
              '%s' % 'https://' + str.replace(row['aditional_image_url_1'], 'y', 'i'),
              '%s' % 'https://' + str.replace(row['aditional_image_url_2'], 'y', 'i'),
              '%s' % 'https://' + str.replace(row['aditional_image_url_3'], 'y', 'i'),
              '%s' % 'https://' + str.replace(row['aditional_image_url_4'], 'y', 'i'),
              '%s' % 'https://' + str.replace(row['aditional_image_url_5'], 'y', 'i'),
              '%s' % 'https://' + str.replace(row['aditional_image_url_6'], 'y', 'i'),
              '%s' % row['google_product_category'])

    mycursor.execute(sql, values)

    if (i % 5000 == 0 and i != 0) or (i + 1 == data_num):

        mydb.commit()

        print('[' + str(i).rjust(data_digits, '0') + '/' + str(data.shape[0]) + '] - Insertion OK')

mydb.close()

print('\nfinished')
