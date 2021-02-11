# ======================================
#exit(0)
# ======================================

from libs import *
import numpy as np

mydb = mysql_connect('database_v3')

#directory = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/teste/vestido longo'
#directory = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/teste/vestido curto'

#directory = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/teste/saia/saia gode evase'
#directory = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/teste/saia/saia lapis'
#directory = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/teste/saia/saia longa'
directory = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/teste/saia/saia midi'

table_skus = 'skus'
field_name = 'cat_1'

cat_name = os.path.basename(directory)

skus_imgs = get_all_file_paths(directory, '.jpg')
skus_imgs.sort()
skus_imgs = np.array(skus_imgs, dtype=str)
skus_imgs_num = len(skus_imgs)
skus_imgs_digits = len(str(skus_imgs_num))

id_skus = []
for img in skus_imgs:

    id_sku = str(int(os.path.basename(img)[10:19]))

    if id_sku.find("'") != '-1':
        id_sku = str.replace(id_sku, "'", "")

    id_skus.append(id_sku)

id_skus = np.array(id_skus, dtype=int)

id_skus = np.unique(id_skus)

if skus_imgs_num == 0:
    print('No files founded, aborted.')
    exit(0)

mycursor = mydb.cursor()

for id_sku in id_skus:

    sql = ' update ' + table_skus + ' set ' + \
          field_name + '=' + '"' + cat_name + '"' \
          ' where id_sku =' + str(id_sku) + ';'
    mycursor.execute(sql)

    mydb.commit()

print(cat_name + ' - update ok')
