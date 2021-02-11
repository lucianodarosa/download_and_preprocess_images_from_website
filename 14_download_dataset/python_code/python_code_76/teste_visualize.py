# ======================================
#exit(0)
# ======================================

import numpy as np
import shutil
from libs import *

mydb = mysql_connect('database_v3')

cat_dir_file = '/media/lucianorosaserver/SSD_SATA_3/mestrado/4_semestre/dissertacao/codigos/14_download_dataset/python_code/python_code_73/updates_4/classes.txt'
logs_dir = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/Untitled Folder/acessorios'
cat_name = 'cat_1'


def find_skus_imgs(_value_cat):

    _sql = ' select skus_imgs.path, skus_imgs.name from skus ' \
           ' inner join skus_imgs ' \
           ' on skus.id_sku = skus_imgs.id_sku ' \
           ' where skus_imgs.download ="Download file ok" ' \
           ' and skus.'+cat_name+' = "'+_value_cat+'"; '
    mydb.reconnect()
    mycursor = mydb.cursor()
    mycursor.execute(_sql)
    _skus = np.array(mycursor.fetchall(), dtype=str)
    return _skus


file1 = open(cat_dir_file, 'r+')
cats_txt = file1.readlines()
cats_result = []
for i, cat in enumerate(cats_txt):
    aux_id = len(cat)
    cats_result.append(cat[0:aux_id].rstrip())
file1.close()

try:
    os.mkdir(logs_dir + slash + cat_name)
except:
    pass

for cat in cats_result:

    distincts = find_skus_imgs(cat)

    folder_cat = logs_dir + slash + cat_name + slash + cat

    try:
        os.mkdir(folder_cat)
    except:
        pass

    for i in distincts:
        shutil.copy(i[0] + slash + i[1], folder_cat + slash + i[1])
