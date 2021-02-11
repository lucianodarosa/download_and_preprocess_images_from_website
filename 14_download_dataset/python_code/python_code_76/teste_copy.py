# ======================================
#exit(0)
# ======================================

from libs import *
import numpy as np
import shutil

mydb = mysql_connect('database_v3')

directory = './updates_3'

logs_dir = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/Untitled Folder/calcados'

table_skus = 'skus'


def find_skus_imgs(_id_sku):

    _sql = ' select skus_imgs.path, skus_imgs.name from skus ' \
           ' inner join skus_imgs ' \
           ' on skus.id_sku = skus_imgs.id_sku ' \
           ' where skus_imgs.download ="Download file ok" ' \
           ' and skus.id_sku = ' + str(_id_sku) + ';'

    mycursor.execute(_sql)
    _skus = np.array(mycursor.fetchall(), dtype=str)
    return _skus

'''
files = os.listdir(directory)
files.sort()
for file in files:
    base = os.path.splitext(file)[0]
    os.rename(directory + slash + file, directory + slash + base + '.txt')
exit(0)
'''

category_files = get_all_file_paths(directory, '.txt')
category_files.sort()
category_files = np.array(category_files, dtype=str)
category_files_num = len(category_files)
category_files_digits = len(str(category_files_num))

if category_files_num == 0:
    print('No files founded, aborted.')
    exit(0)

mycursor = mydb.cursor()

for category_file in category_files:

    cat_name = os.path.basename(category_file)
    cat_name = os.path.splitext(cat_name)[0]

    folder_cat = logs_dir + slash + cat_name
    os.mkdir(folder_cat)

    file1 = open(category_file, 'r+')
    skus = file1.readlines()
    id_skus = []
    for sku in skus:
        if bool(sku and sku.strip()):

            id_sku = sku[:sku.find(',')]
            if id_sku.find("'") != '-1':
                id_sku = str.replace(id_sku, "'", "")

            skus_imgs = find_skus_imgs(id_sku)

            for i in skus_imgs:
                shutil.copy(i[0] + slash + i[1], folder_cat + slash + i[1])

    file1.close()

    mydb.commit()
