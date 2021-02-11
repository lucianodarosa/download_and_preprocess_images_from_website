# ======================================
exit(0)
# ======================================

import numpy as np
from libs import *

mydb = mysql_connect('database_v3')


def find_distinct():

    '''
    _sql = ' SELECT val, COUNT(*) AS total ' \
           ' FROM (SELECT cat_1 AS Val FROM skus ' \
           '       where cat_1 is not null) AS T  ' \
           ' GROUP BY val '
    '''

    '''
    _sql = ' SELECT val, COUNT(*) AS total ' \
           ' FROM (SELECT cat_2 AS Val FROM skus ' \
           '       where cat_2 is not null) AS T  ' \
           ' GROUP BY val '
    '''

    '''
    _sql = ' SELECT val, COUNT(*) AS total ' \
           ' FROM (SELECT cat_3 AS Val FROM skus ' \
           '       where cat_3 is not null) AS T  ' \
           ' GROUP BY val '
    '''

    '''
    _sql = ' SELECT val, COUNT(*) AS total ' \
           ' FROM (SELECT cat_4 AS Val FROM skus ' \
           '       where cat_4 is not null) AS T  ' \
           ' GROUP BY val '
    '''

    '''
    _sql = ' SELECT val, COUNT(*) AS total ' \
           ' FROM (SELECT cat_5 AS Val FROM skus ' \
           '       where cat_5 is not null) AS T  ' \
           ' GROUP BY val '
    '''

    '''
    _sql = ' SELECT val, COUNT(*) AS total ' \
           ' FROM (SELECT cat_6 AS Val FROM skus ' \
           '       where cat_6 is not null) AS T  ' \
           ' GROUP BY val '
    '''

    '''
    _sql = ' SELECT val, COUNT(*) AS total ' \
           ' FROM (SELECT main_category AS Val FROM skus ' \
           '       where main_category is not null) AS T  ' \
           ' GROUP BY val '
    '''

    '''
    _sql = ' SELECT val, COUNT(*) AS total ' \
           ' FROM (SELECT sub_category AS Val FROM skus ' \
           '       where sub_category is not null) AS T  ' \
           ' GROUP BY val '
    '''

    #'''
    _sql = ' SELECT val, COUNT(*) AS total ' \
           ' FROM (SELECT google_product_category AS Val FROM skus ' \
           '       where google_product_category is not null) AS T  ' \
           ' GROUP BY val '
    #'''

    '''
    _sql = ' SELECT val, COUNT(*) AS total ' \
           ' FROM (SELECT cat_1 AS Val FROM skus ' \
           '       where cat_1 is not null ' \
           '       UNION ALL ' \
           '       SELECT cat_2 AS Val FROM skus ' \
           '       where cat_2 is not null ' \
           '       UNION ALL ' \
           '       SELECT cat_3 AS Val FROM skus ' \
           '       where cat_3 is not null ' \
           '       UNION ALL ' \
           '       SELECT cat_4 AS Val FROM skus ' \
           '       where cat_4 is not null ' \
           '       UNION ALL ' \
           '       SELECT cat_5 AS Val FROM skus ' \
           '       where cat_5 is not null ' \
           '       UNION ALL ' \
           '       SELECT cat_6 AS Val FROM skus ' \
           '       where cat_6 is not null ' \
           '       UNION ALL ' \
           '       SELECT main_category AS Val FROM skus ' \
           '       where main_category is not null ' \
           '       UNION ALL ' \
           '       SELECT sub_category AS Val FROM skus ' \
           '       where sub_category is not null) AS T ' \
           ' GROUP BY val '
           #' order by total desc;'
    '''

    mydb.reconnect()
    mycursor = mydb.cursor()
    mycursor.execute(_sql)
    _skus = np.array(mycursor.fetchall(), dtype=str)
    return _skus


distincts = find_distinct()

count = 0
for i in distincts:
    print(i)
    count += int(i[1])

#print(count)
#exit(0)

len_max = 0
for i in distincts:
    if len_max < len(i[0]):
        len_max = len(i[0])

file1 = open('/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/verify_labels_logs/count_google_product_category.txt', 'w')

for i in distincts:
    teste = i[0].ljust(len_max + 5) + i[1]
    file1.write(teste + '\n')
file1.close()
