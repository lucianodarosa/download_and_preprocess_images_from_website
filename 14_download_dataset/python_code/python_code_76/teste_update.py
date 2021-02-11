# ======================================
#exit(0)
# ======================================

from libs import *
import numpy as np

mydb = mysql_connect('database_v3')

directory = './updates_2'
table_skus = 'skus'
field_name = 'product_name'
field_val_old = 'capas de almofadas'
field_val_new = 'capa de almofada'

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

labels = []
values = []

mycursor = mydb.cursor()

for category_file in category_files:

    file1 = open(category_file, 'r+')
    skus = file1.readlines()
    id_skus = []
    for sku in skus:
        if bool(sku and sku.strip()):

            id_sku = sku[:sku.find(',')]
            if id_sku.find("'") != '-1':
                id_sku = str.replace(id_sku, "'", "")

            value_ant = sku[sku.find(',') + 1:]
            if value_ant.find("'") != '-1':
                value_ant = str.replace(value_ant, "'", "")

            if value_ant.find(",") != '-1':
                value_ant = value_ant[:value_ant.find(',')]

            value_before = str.replace(value_ant, field_val_old, field_val_new)
            value_before = value_before.strip()

            #print(id_sku)
            #print(value_ant)
            #print(value_before)
            #exit(0)

            sql = ' update ' + table_skus + ' set ' + \
                  field_name + '=' + '"' + value_before + '"' \
                  ' where id_sku =' + str(id_sku) + ';'
            mycursor.execute(sql)

            print(str(id_sku) + ' - update OK')

    file1.close()

    mydb.commit()
