# ======================================
#exit(0)
# ======================================

from libs import *
import shutil

#origem = '/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/raw/street2shop/photos/'
#destino = '/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/raw/street2shop_2/photos/'

origem = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/verify_labels_logs/sub_category_remove'

destino = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/verify_labels_logs/all'

imgs_paths = get_all_file_paths(origem, '.jpg')
imgs_paths.sort()
imgs_paths_num = len(imgs_paths)

if imgs_paths_num == 0:
    print('No files founded, aborted.')
    exit(0)


for i, img_path in enumerate(imgs_paths):

    name = os.path.basename(img_path)

    #shutil.move(img_path, destino + slash + name)
    shutil.copy(img_path, destino + slash + name)

    print(str(i + 1) + slash + str(imgs_paths_num) + ' - OK')
