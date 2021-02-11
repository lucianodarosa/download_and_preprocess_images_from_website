# ======================================
#exit(0)
# ======================================

import numpy as np
from libs import *

mydb = mysql_connect('database_v3')
mydb2 = mysql_connect('database_v4')

def find_skus():

    _sql = ' select id_sku, product_name, cat_1, cat_2, cat_3, cat_4, cat_5, cat_6, ' \
           ' main_category, sub_category, gender, google_product_category '\
           ' from skus;'
    mydb.reconnect()
    mycursor = mydb.cursor()
    mycursor.execute(_sql)
    _skus = np.array(mycursor.fetchall(), dtype=str)
    return _skus


skus = find_skus()
skus_num = len(skus)
skus_num_digits = len(str(skus_num))


mycursor = mydb2.cursor()

for i, sku in enumerate(skus):

    '''
    _sql = ' update skus set ' + \
           ' cat_1 = "' + sku[1] + '",' + \
           ' cat_2 = "' + sku[2] + '",' + \
           ' cat_3 = "' + sku[3] + '",' + \
           ' cat_4 = "' + sku[4] + '",' + \
           ' cat_5 = "' + sku[5] + '",' + \
           ' cat_6 = "' + sku[6] + '",' + \
           ' main_category = "' + sku[7] + '",' + \
           ' sub_category = "' + sku[8] + '",' + \
           ' gender = "' + sku[9] + '",' + \
           ' google_product_category = "' + sku[10] + '"' + \
           ' where id_sku = ' + str(sku[0])
    '''

    #'''
    _sql = ' update skus set ' + \
           ' product_name = "' + sku[1] + '",' + \
           ' cat_1 = "' + sku[2] + '"' + \
           ' where id_sku = ' + str(sku[0]) + ';'
    mycursor.execute(_sql)
    #'''

    if (i % 5000 == 0 and i != 0) or (i + 1 == skus_num):

        mydb2.commit()

        print('[' + str(i + 1).rjust(skus_num_digits, '0') + '/' + str(skus_num) + '] - update OK')
