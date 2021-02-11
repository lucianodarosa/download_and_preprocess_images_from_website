# CHECK_01 - CONVERSÃO PARA FORMATO PADRÃO
# CONVERTE E SALVA TODAS AS IMAGENS PARA O FORMATO .JPG
# ELIMINA OS CAMINHOS ANTIGOS, REPORTA FALHAS E ATUALIZA STATUS DE CHECAGEM NO DATABASE

# ======================================
exit(0)
# ======================================

from multiprocessing import Pool
import time
import numpy as np
from shutil import copyfile
from PIL import Image
from libs import *

mydb = mysql_connect('database_v2')

table_skus_imgs = 'skus_imgs'
logs_dir = './logs_check_1/'
field_check = 'check_1'
ext_out = '.jpg'
pool_size = 12


def find_skus_imgs():

    _sql = ' select id_img, id_sku, id_num, url, name, path '\
           ' from ' + table_skus_imgs + \
           ' where download = "Download file ok" ' \
           ' and ' + field_check + ' is null '#\
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
        _name_quote, _ext_in = os.path.splitext(_name)

        _id_aux = np.where(skus_imgs[:, 0] == _sku_img[0])[0][0]
        _progress = '[' + str(_id_aux + 1).rjust(skus_imgs_digits, '0') + '/' + str(skus_imgs_num) + '] - '

        _corrupt = 0
        _updated = 0

        # ====================

        try:

            img = Image.open(_path + slash + _name)
            img.convert('RGB').save(_path + slash + _name_quote + ext_out)
            img.close()

            if _ext_in != ext_out:
                os.remove(_path + slash + _name)

                _sql = ' update ' + table_skus_imgs + ' set ' \
                       ' name = "' + _name_quote + ext_out + '"' \
                       ' where id_img = ' + str(_id_img) + ';'
                mydb.reconnect()
                mycursor = mydb.cursor()
                mycursor.execute(_sql)
                mydb.commit()

                _updated = 1

        except:
            _corrupt = 1

        # ====================

        if _corrupt == 1:

            print(_progress + 'img corrupted: ' + _path + slash + _name)
            copyfile(_path + slash + _name, logs_dir + _name)

        else:

            if _updated == 1:
                print(_progress + 'img ext updated: ' + _path + slash + _name)
            else:
                print(_progress + 'img OK')

        #'''
        _sql = ' update ' + table_skus_imgs + ' set ' \
               ' ' + field_check + ' = ' + str(_corrupt) + \
               ' where id_img = ' + str(_id_img) + ';'
        mydb.reconnect()
        mycursor = mydb.cursor()
        mycursor.execute(_sql)
        mydb.commit()
        #'''

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
