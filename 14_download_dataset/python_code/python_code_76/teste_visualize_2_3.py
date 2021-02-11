# ======================================
#exit(0)
# ======================================

from libs import *
import numpy as np

mydb = mysql_connect('database_v3')

directory = './updates'
table_skus = 'skus'
field_name = 'cat_1'

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

    cat_name, _ = os.path.splitext(os.path.basename(category_file))

    file1 = open(category_file, 'r+')
    skus = file1.readlines()

    for sku in skus:
        if bool(sku and sku.strip()):

            id_sku = sku[:sku.find(',')]

            if id_sku.find("'") != '-1':
                id_sku = str.replace(id_sku, "'", "")

            #print(cat_name)
            #print(id_sku)
            #exit(0)

            sql = ' update ' + table_skus + ' set ' + \
                  field_name + '=' + '"' + cat_name + '"' \
                  ' where id_sku =' + str(id_sku) + ';'
            mycursor.execute(sql)

    file1.close()

    mydb.commit()

    print(cat_name + ' - update ok')
