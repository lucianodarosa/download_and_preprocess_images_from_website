# ======================================
exit(0)
# ======================================

from multiprocessing import Pool
import time
import numpy as np
from libs import *

mydb = mysql_connect('database_v2')

#directory = '/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/photos_3/'

#directory = '/media/lucianorosaserver/SSD_SATA_3_2/datasets/01_DeepFashion_new/Category and Attribute Prediction Benchmark/Img/img_highres'
#directory = '/media/lucianorosaserver/SSD_SATA_3_2/datasets/01_DeepFashion_new/Consumer-to-shop Clothes Retrieval Benchmark/Img/img_highres'
#directory = '/media/lucianorosaserver/SSD_SATA_3_2/datasets/01_DeepFashion_new/In-shop Clothes Retrieval Benchmark/Img/img_highres'

#directory = '/media/lucianorosaserver/SSD_SATA_3/datasets/02_DeepFashion2/validation/image'
#directory = '/media/lucianorosaserver/SSD_SATA_3/datasets/02_DeepFashion2/train/image'

table_aux_imgs = 'aux_imgs6'
pool_size = 12


class VerifyFiles(object):

    def get_file(self, _img_path):

        name = os.path.basename(_img_path)
        path = _img_path.replace(name, '')

        _id_aux = np.where(imgs_paths == _img_path)[0][0]
        _progress = '[' + str(_id_aux + 1).rjust(imgs_paths_digits, '0') + '/' + str(imgs_paths_num) + '] - '

        sql = ' insert into ' + table_aux_imgs + \
              ' (name, path) ' \
              ' values ("' + name + '", "' + path + '");'
        mydb.reconnect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()

        print(_progress + 'img insert OK')

    def Verify(self):

        pool = Pool(pool_size)
        pool.map(self.get_file, imgs_paths)
        pool.close()
        pool.join()
        pool.terminate()
        del pool


imgs_paths = get_all_file_paths(directory, '.jpg')
imgs_paths.sort()
imgs_paths = np.array(imgs_paths, dtype=str)
imgs_paths_num = len(imgs_paths)
imgs_paths_digits = len(str(imgs_paths_num))

if imgs_paths_num == 0:
    print('No files founded, aborted.')
    exit(0)

print('\n ===================================== ini insertion\n')

start_time_batch = time.time()

d = VerifyFiles()
d.Verify()

end_time_batch = time.time() - start_time_batch

# calculate and show time
days_batch, remainder = divmod(end_time_batch, 86400)
hours_batch, remainder = divmod(remainder, 3600)
minutes_batch, seconds_batch = divmod(remainder, 60)
msg = '(%02dd:%02dh:%02dm:%02ds' % (days_batch, hours_batch, minutes_batch, seconds_batch) + ')'
print('\n ===================================== end insertion: ' + msg)
