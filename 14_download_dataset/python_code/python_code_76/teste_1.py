# ======================================
#exit(0)
# ======================================

import time
import numpy as np
import re
import sys
from libs import *

mydb = mysql_connect('database_v4')

special_chars = ['á', 'Á', 'ã', 'Ã', 'â', 'Â', 'à', 'À', 'ä', 'Ä', 'é', 'É', 'ê', 'Ê', 'ë', 'Ë', 'è', 'È', 'í', 'Í',
                 'ï', 'Ï', 'ì', 'Ì', 'î', 'Î', 'ó', 'Ó', 'õ', 'Õ', 'ô', 'Ô', 'ö', 'Ö', 'ò', 'Ò', 'ú', 'Ú', 'ü', 'Ü',
                 'ù', 'Ù', 'û', 'Û', 'ç', 'Ç', 'ñ', 'Ñ', 'ý', 'Ý', 'ÿ', 'Ÿ']

normal_chars = ['a', 'A', 'a', 'A', 'a', 'A', 'a', 'A', 'a', 'A', 'e', 'E', 'e', 'E', 'e', 'E', 'e', 'E', 'i', 'I',
                'i', 'I', 'i', 'I', 'i', 'I', 'o', 'O', 'o', 'O', 'o', 'O', 'o', 'O', 'o', 'O', 'u', 'U', 'u', 'U',
                'u', 'U', 'u', 'U', 'c', 'C', 'n', 'N', 'y', 'Y', 'y', 'Y']

fields = ['product_name', 'cat_1', 'cat_2', 'cat_3', 'cat_4', 'cat_5', 'cat_6', 'main_category', 'sub_category', 'gender', 'google_product_category']


def find_skus():

    _sql = ' select id_sku, product_name, cat_1, cat_2, cat_3, cat_4, cat_5, cat_6, ' \
           ' main_category, sub_category, gender, google_product_category '\
           ' from skus'
    mydb.reconnect()
    mycursor = mydb.cursor()
    mycursor.execute(_sql)
    _skus = np.array(mycursor.fetchall(), dtype=str)
    return _skus

field_id = 0
'''
try:
    field_id = int(sys.argv[1])
except:
    exit(0)
'''

skus = find_skus()
skus_num = len(skus)
skus_num_digits = len(str(skus_num))

mycursor = mydb.cursor()

start_time_batch = time.time()

for i, sku in enumerate(skus):

    string_val = sku[field_id + 1]

    _progress = '[' + str(i + 1).rjust(skus_num_digits, '0') + '/' + str(skus_num) + '] - '

    # replace accentuation characters
    for j in range(len(special_chars)):
        string_val = string_val.replace(special_chars[j], normal_chars[j])

    if field_id != 9:
        # remove special characters
        string_val = re.sub('[^a-zA-Z0-9 ]', '', string_val)

    # remove whitespaces
    string_val = string_val.strip()

    if string_val != 'none' and string_val != 'None':

        #'''
        # update value into mysql
        _sql = ' update skus set ' + \
               fields[field_id] + ' = "' + string_val + \
               '" where id_sku = ' + str(sku[0])+';'
        mycursor.execute(_sql)
        #'''

    if (i % 5000 == 0 and i != 0) or (i + 1 == skus_num):

        mydb.commit()

    print(_progress + 'sku update (' + str(field_id) + '-' + str(fields[field_id]) + ') OK')

end_time_batch = time.time() - start_time_batch

# calculate and show time
days_batch, remainder = divmod(end_time_batch, 86400)
hours_batch, remainder = divmod(remainder, 3600)
minutes_batch, seconds_batch = divmod(remainder, 60)
msg = '(%02dd:%02dh:%02dm:%02ds' % (days_batch, hours_batch, minutes_batch, seconds_batch) + ')'
print('\n ===================================== end: ' + msg)
