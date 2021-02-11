# ATUALIZA OS CAMINHOS DAS IMAGENS NO DATABASE

# ======================================
exit(0)
# ======================================

from libs import *

mydb = mysql_connect('database_v4')

dataset_path = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/images/images_v3'
table_skus_imgs = 'skus_imgs'

skus_imgs = get_all_file_paths(dataset_path, '.jpg')
skus_imgs.sort()
skus_imgs_num = len(skus_imgs)
skus_imgs_digits = len(str(skus_imgs_num))

if skus_imgs_num == 0:
    print('No files founded, aborted.')
    exit(0)

skus_imgs_count = 0

mycursor = mydb.cursor()

print()
for img_path in skus_imgs:

    id_img = int(os.path.basename(img_path)[0:9])
    path = os.path.dirname(img_path)

    sql = ' update ' + table_skus_imgs + ' set ' \
          ' path="' + path + '" ' \
          ' where id_img = ' + str(id_img) + ';'
    mycursor.execute(sql)

    if (skus_imgs_count % 5000 == 0 and skus_imgs_count != 0) or (skus_imgs_count + 1 == skus_imgs_num):

        mydb.commit()

        print('[' + str(skus_imgs_count).rjust(skus_imgs_digits, '0') + '/' + str(skus_imgs_num) + '] - update OK')

    skus_imgs_count += 1

mydb.close()
