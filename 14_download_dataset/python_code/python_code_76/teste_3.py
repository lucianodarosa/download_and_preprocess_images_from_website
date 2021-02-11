# ======================================
#exit(0)
# ======================================

import numpy as np
from libs import *

mydb = mysql_connect('database_v3')

#fields = ['cat_1', 'cat_2', 'cat_3', 'cat_4', 'cat_5', 'cat_6', 'main_category', 'sub_category', 'gender', 'google_product_category']
fields = ['cat_1']


def find_skus():

    _sql = ' select id_sku, cat_1, cat_2, cat_3, cat_4, cat_5, cat_6, ' \
           ' main_category, sub_category, gender, google_product_category '\
           ' from skus'
    mydb.reconnect()
    mycursor = mydb.cursor()
    mycursor.execute(_sql)
    _skus = np.array(mycursor.fetchall(), dtype=str)
    return _skus


field_id = 0

skus = find_skus()
skus_num = len(skus)
skus_num_digits = len(str(skus_num))

mycursor = mydb.cursor()

list_terms = []
for i, sku in enumerate(skus):

    cat_val = sku[field_id + 1]

    for j, field in enumerate(fields):

        if sku[j + 1] != 'None' and sku[j + 1] != 'none' and j != field_id:

            aux_val = sku[j + 1]

            if cat_val == aux_val:

                value_aux = '(' + str(fields[field_id]) + ' - ' + str(fields[j]) + ')'
                print(value_aux)
                list_terms.append(value_aux)

                #'''
                _sql = ' update skus set ' \
                       + fields[j] + ' = null ' \
                       ' where id_sku = ' + str(sku[0])+';'
                mycursor.execute(_sql)
                mydb.commit()
                #'''

np.savetxt('./dups/dups_' + fields[field_id] + '.txt', list_terms, fmt="%s")
