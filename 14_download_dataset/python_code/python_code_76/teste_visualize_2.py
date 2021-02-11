# ======================================
#exit(0)
# ======================================

from libs import *

mydb = mysql_connect('database_v3')

cat_dir_file = '/media/lucianorosaserver/SSD_SATA_3/mestrado/4_semestre/dissertacao/codigos/14_download_dataset/python_code/python_code_66/updates_3/update.txt'
table_skus = 'skus'
field_name = 'sub_category'
field_value = 'null'


file1 = open(cat_dir_file, 'r+')
skus = file1.readlines()

id_skus = []
for sku in skus:

    if bool(sku and sku.strip()):

        id_sku = sku[:sku.find(',')]

        if id_sku.find("'") != '-1':
            id_sku = str.replace(id_sku, "'", "")

        id_skus.append(id_sku)

file1.close()

mycursor = mydb.cursor()

for id_sku in id_skus:

    #print(id_sku)
    #exit(0)

    sql = ' update ' + table_skus + ' set ' + \
          field_name + '=null' + \
          ' where id_sku =' + str(id_sku) + ';'
    mycursor.execute(sql)
    mydb.commit()

    '''
    sql = ' update ' + table_skus + ' set ' + \
          field_name + '=' + '"' + field_value + '"'  \
          ' where id_sku =' + str(id_sku) + ';'
    mycursor.execute(sql)
    mydb.commit()
    '''
