# GERA E SALVA NO DATABASE O CÓDIGO HASH (PERCEPTUAL HASH) DE CADA IMAGEM
# SÃO GERADOS E CONCATENADOS O HASH DE CADA DIMENSÃO RGB

# ======================================
exit(0)
# ======================================

from multiprocessing import Pool
import time
import numpy as np
from PIL import Image
from imagehash import phash
from libs import *

mydb = mysql_connect('database_v2')

table_skus_imgs = 'skus_imgs'
pool_size = 12


def get_phash(_filepath):

    _img = Image.open(_filepath).convert('RGB')
    _r, _g, _b = _img.split()

    _h_hex_r = str(phash(image=_r, hash_size=16))
    _h_hex_g = str(phash(image=_g, hash_size=16))
    _h_hex_b = str(phash(image=_b, hash_size=16))

    _h_int_r = int(_h_hex_r, 16)
    _h_int_g = int(_h_hex_g, 16)
    _h_int_b = int(_h_hex_b, 16)

    _h_bin_r = bin(_h_int_r)[2:]
    _h_bin_g = bin(_h_int_g)[2:]
    _h_bin_b = bin(_h_int_b)[2:]

    _r.close()
    _g.close()
    _b.close()
    _img.close()

    return _h_bin_r + _h_bin_r + _h_bin_r


def find_skus_imgs():

    _sql = ' select id_img, id_sku, id_num, url, name, path '\
           ' from ' + table_skus_imgs + \
           ' where download = "Download file ok" ' \
           ' and hash is null; ' #\
           #' limit 10000;'
    mydb.reconnect()
    mycursor = mydb.cursor()
    mycursor.execute(_sql)
    _skus_images = np.array(mycursor.fetchall(), dtype=str)
    return _skus_images


class VerifyFiles(object):

    def get_file(self, _sku_img):

        _id_img = _sku_img[0]
        _name = _sku_img[4]
        _path = _sku_img[5]

        _id_aux = np.where(skus_imgs[:, 0] == _sku_img[0])[0][0]
        _progress = '[' + str(_id_aux + 1).rjust(skus_imgs_digits, '0') + '/' + str(skus_imgs_num) + '] - '

        hash = get_phash(_path + slash + _name)

        #'''
        _sql = ' update ' + table_skus_imgs + ' set ' \
               ' hash ="' + hash + '" ' \
               ' where id_img = ' + str(_id_img) + ';'
        mydb.reconnect()
        mycursor = mydb.cursor()
        mycursor.execute(_sql)
        mydb.commit()
        #'''

        print(_progress + 'OK')

    def Verify(self):

        pool = Pool(pool_size)
        pool.map(self.get_file, skus_imgs)
        pool.close()
        pool.join()
        pool.terminate()
        del pool


skus_imgs = find_skus_imgs()
skus_imgs_num = len(skus_imgs)
skus_imgs_digits = len(str(skus_imgs_num))

#while skus_imgs_num > 0:

#time.sleep(10)  # 10secs
#time.sleep(600)  # 10*60secs = 10min

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

#exit(0)

#skus_imgs = find_skus_imgs()
#skus_imgs_num = len(skus_imgs)
#skus_imgs_digits = len(str(skus_imgs_num))

mydb.close()
