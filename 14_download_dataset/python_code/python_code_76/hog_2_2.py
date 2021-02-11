# GERA E SALVA NO DATABASE O CÓDIGO HASH (PERCEPTUAL HASH) DE CADA IMAGEM
# SÃO GERADOS E CONCATENADOS O HASH DE CADA DIMENSÃO RGB

# ======================================
#exit(0)
# ======================================

from multiprocessing import Pool
import time
import numpy as np
from libs import *
from skimage.io import imread
from skimage.transform import resize
from skimage.feature import hog

class_name = 'mocassim'
imgs_dir = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/Untitled Folder/calcados/' + class_name
descriptors_dir = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/logs_hog/' + class_name + '/descriptors'
pool_size = 12


def extract_hog(_img_path):

    _img = imread(_img_path)
    resized_img = resize(_img, (128, 64))

    dp, _ = hog(resized_img, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=True, multichannel=True)

    return dp


class VerifyFiles(object):

    def get_file(self, _img_path):

        filename = os.path.basename(_img_path)
        ext = os.path.splitext(filename)[1]
        name = str.replace(filename, ext, '')

        _id_aux = np.where(imgs_paths == _img_path)[0][0]
        _progress = '[' + str(_id_aux + 1).rjust(skus_imgs_digits, '0') + '/' + str(imgs_paths_num) + '] - '

        goods = extract_hog(_img_path)

        np.savetxt(descriptors_dir + slash + str(name) + '.out', goods)

        print(_progress + 'OK')

    def Verify(self):

        pool = Pool(pool_size)
        pool.map(self.get_file, imgs_paths)
        pool.close()
        pool.join()
        pool.terminate()
        del pool


imgs_paths = get_all_file_paths(imgs_dir, '.jpg')
imgs_paths.sort()
imgs_paths = np.array(imgs_paths, dtype=np.str)
imgs_paths_num = len(imgs_paths)
skus_imgs_digits = len(str(imgs_paths_num))

if imgs_paths_num == 0:
    print('No files founded, aborted.')
    exit(0)

print('\n ===================================== ini check\n')

start_time_batch = time.time()

d = VerifyFiles()
d.Verify()

end_time_batch = time.time() - start_time_batch

# calculate and show time
days_batch, remainder = divmod(end_time_batch, 86400)
hours_batch, remainder = divmod(remainder, 3600)
minutes_batch, seconds_batch = divmod(remainder, 60)
msg = '(%02dd:%02dh:%02dm:%02ds' % (days_batch, hours_batch, minutes_batch, seconds_batch) + ')'
print('\n ===================================== end check: ' + msg)
