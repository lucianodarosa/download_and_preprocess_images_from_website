# CHECK_03 - VERIFICAÇÕES  DE PADRÕES DE COR
# VERIFICA A EXISTÊNCIA DE UM PADRÃO DE COR ESPECÍFICO (IMAGEM CORROMPIDA)
# REPORTA FALHAS E ATUALIZA STATUS DE CHECAGEM NO DATABASE

# ======================================
exit(0)
# ======================================

from multiprocessing import Pool
import time
import numpy as np
from shutil import copyfile
from libs import *

mydb = mysql_connect('database_v2')

table_skus_imgs = 'skus_imgs'
logs_dir = './logs_check_3/'
field_check = 'check_3'
pool_size = 12

prct_corrupt = 1
color_corrupt = [128, 128, 128]


def is_solid(_array_pixels, _order: int = 1, _color_corrupt=color_corrupt):

    if _order == -1:
        _array_pixels = np.flipud(_array_pixels)

    _count = 0
    for _pixel in _array_pixels[0:3]:

        if np.array_equal(_pixel, _color_corrupt):
            _count += 1
        else:
            break

    if _count == 3:
        return True
    else:
        return False


def is_corrupted(_file, _color_corrupt=color_corrupt, _prct=prct_corrupt):

    _img = cv2.imread(_file)
    _rows = _img.shape[0]
    _cols = _img.shape[1]
    _color_count = np.sum(_img == _color_corrupt) // 3
    _prct_result = (_color_count * 100) / (_rows * _cols)

    if _prct_result >= _prct:

        _top = _img[0, :]
        _botton = _img[_rows - 1, :]
        _left = _img[:, 0]
        _right = _img[:, _cols - 1]

        _top_count = np.sum(_top == _color_corrupt) // 3
        _botton_count = np.sum(_botton == _color_corrupt) // 3
        _left_count = np.sum(_left == _color_corrupt) // 3
        _right_count = np.sum(_right == _color_corrupt) // 3

        if _top_count == _cols or _botton_count == _cols or _left_count == _rows or _right_count == _rows:
            return True
        else:
            _top_left = _top[0]
            _top_right = _top[_cols - 1]
            _botton_left = _botton[0]
            _botton_right = _botton[_cols - 1]

            _top_left_color = np.array_equal(_top_left, _color_corrupt)
            _top_right_color = np.array_equal(_top_right, _color_corrupt)
            _botton_left_color = np.array_equal(_botton_left, _color_corrupt)
            _botton_right_color = np.array_equal(_botton_right, _color_corrupt)

            if not _top_left_color and not _top_right_color and not _botton_left_color and not _botton_right_color:
                return False
            else:
                _top_left_right = is_solid(_top, 1, _color_corrupt)
                _top_right_left = is_solid(_top, -1, _color_corrupt)
                _left_top_botton = is_solid(_left, 1, _color_corrupt)
                _left_botton_top = is_solid(_left, -1, _color_corrupt)
                _right_top_botton = is_solid(_right, 1, _color_corrupt)
                _right_botton_top = is_solid(_right, -1, _color_corrupt)
                _botton_left_right = is_solid(_botton, 1, _color_corrupt)
                _botton_right_left = is_solid(_botton, -1, _color_corrupt)

                if (_top_left_right != _top_right_left) or (_left_top_botton != _left_botton_top) or \
                        (_right_top_botton != _right_botton_top) or (_botton_left_right != _botton_right_left):
                    return True
                else:
                    return False
    else:
        return False


def find_skus_imgs():

    _sql = ' select id_img, id_sku, id_num, url, name, path '\
           ' from ' + table_skus_imgs + \
           ' where download = "Download file ok" ' \
           ' and check_1=0 ' \
           ' and check_2=0 ' \
           ' and ' + field_check + ' is null;'
           #' limit 5000;'
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

        _corrupt = 0

        # ====================

        _result = is_corrupted(_path + slash + _name, color_corrupt, prct_corrupt)
        if _result:
            _corrupt = 1

        # ====================

        if _corrupt == 1:
            print(_progress + 'img corrupted: ' + _path + slash + _name)
            copyfile(_path + slash + _name, logs_dir + _name)

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
