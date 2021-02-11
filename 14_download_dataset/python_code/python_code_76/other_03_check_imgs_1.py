# ======================================
exit(0)
# ======================================

import time
from multiprocessing import Pool
import numpy as np
from PIL import Image
from shutil import copyfile
from libs import *

mydb = mysql_connect('database_v2')

table_aux_imgs = 'aux_imgs6'
logs_dir = './logs_check_1/'
field_check = 'check_1'
ext_out = '.jpg'
pool_size = 12


def find_imgs_paths():

    _sql = ' select id_img, name, path '\
           ' from ' + table_aux_imgs + \
           ' where ' + field_check + ' is null '\
           ' order by id_img'
    mydb.reconnect()
    mycursor = mydb.cursor()
    mycursor.execute(_sql)
    _imgs_paths = np.array(mycursor.fetchall(), dtype=str)
    return _imgs_paths


class VerifyFiles(object):

    def get_file(self, _img_path):

        _id_img = _img_path[0]
        _name = _img_path[1]
        _path = _img_path[2]
        _name_quote, _ext_in = os.path.splitext(_name)

        _id_aux = np.where(imgs_paths[:, 0] == _img_path[0])[0][0]
        _progress = '[' + str(_id_aux + 1).rjust(imgs_paths_digits, '0') + '/' + str(imgs_paths_num) + '] - '

        _corrupt = 0
        _updated = 0
        try:

            img = Image.open(_path + _name)
            img.convert('RGB').save(_path + _name_quote + ext_out)
            img.close()

            if _ext_in != ext_out:

                os.remove(_path + _name)

                _sql = ' update ' + table_aux_imgs + ' set ' \
                       ' name = "' + _name_quote + ext_out + '"' \
                       ' where id_img = ' + str(_id_img) + ';'
                mydb.reconnect()
                mycursor = mydb.cursor()
                mycursor.execute(_sql)
                mydb.commit()

                _updated = 1

        except:
            _corrupt = 1

        if _corrupt == 1:

            print(_progress + 'img corrupted: ' + _path + _name)

            _name_out = logs_dir + _name
            if os.path.isfile(_name_out):
                _name_out = logs_dir + _name_quote + '_' + _id_img + _ext_in
            copyfile(_path + _name, _name_out)

            _sql = ' update ' + table_aux_imgs + ' set ' \
                   ' ' + field_check + ' =1 ' \
                   ' where id_img = ' + str(_id_img) + ';'
            mydb.reconnect()
            mycursor = mydb.cursor()
            mycursor.execute(_sql)
            mydb.commit()

        else:

            if _updated == 1:
                print(_progress + 'img ext updated: ' + _path + _name)
            else:
                print(_progress + 'img OK')

    def Verify(self):

        pool = Pool(pool_size)
        pool.map(self.get_file, imgs_paths)
        pool.close()
        pool.join()
        pool.terminate()
        del pool


imgs_paths = find_imgs_paths()
imgs_paths_num = len(imgs_paths)
imgs_paths_digits = len(str(imgs_paths_num))

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

mydb.close()
