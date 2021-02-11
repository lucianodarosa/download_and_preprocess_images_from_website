# ======================================
exit(0)
# ======================================

import numpy as np
from libs import *

mydb = mysql_connect('database_v2')

fields = ['cat_1', 'cat_2', 'cat_3', 'cat_4', 'cat_5', 'cat_6', 'main_category', 'sub_category', 'gender', 'google_product_category']


def find_distinct(_field: str):

    _sql = ' select distinct(' + _field + ') ' +\
           ' from skus ' +\
           ' where ' + _field + ' is not null ' +\
           ' group by ' + _field
    mydb.reconnect()
    mycursor = mydb.cursor()
    mycursor.execute(_sql)
    _skus = np.array(mycursor.fetchall(), dtype=str)
    return _skus


aux01 = find_distinct(fields[0]).flatten()
aux02 = find_distinct(fields[1]).flatten()
aux03 = find_distinct(fields[2]).flatten()
aux04 = find_distinct(fields[3]).flatten()
aux05 = find_distinct(fields[4]).flatten()
aux06 = find_distinct(fields[5]).flatten()
aux07 = find_distinct(fields[6]).flatten()
aux08 = find_distinct(fields[7]).flatten()
aux09 = find_distinct(fields[8]).flatten()
aux10 = find_distinct(fields[9]).flatten()

#aux_final = np.concatenate((aux01, aux02, aux03, aux04, aux05, aux06, aux07, aux08, aux09, aux10))
aux_final = np.concatenate((aux01, aux02, aux03, aux04, aux05, aux06, aux07, aux08))
aux_final.sort()

aux_final = np.unique(aux_final)

for i in aux_final:
    print(i)

#np.savetxt('./dups/all_info.txt', aux_final, fmt="%s")
np.savetxt('./dups/all_info_without_gender_and_google_cat.txt', aux_final, fmt="%s")
