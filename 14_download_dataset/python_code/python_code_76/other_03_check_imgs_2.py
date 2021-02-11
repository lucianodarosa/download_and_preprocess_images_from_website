# ======================================
exit(0)
# ======================================

from multiprocessing import Pool
import time
import numpy as np
from PIL import Image
import PIL
from subprocess import Popen, PIPE
from shutil import copyfile
from libs import *

mydb = mysql_connect('database_v2')

table_aux_imgs = 'aux_imgs6'
logs_dir = './logs_check_2/'
field_check = 'check_1'
pool_size = 12


def find_imgs_paths():

    #_sql = ' select id_img, name, path '\
    #       ' from ' + table_aux_imgs + \
    #       ' where ' + field_check + ' is null '\
    #       ' order by id_img'

    _sql = ' select id_img, name, path '\
          ' from ' + table_aux_imgs
    mydb.reconnect()
    mycursor = mydb.cursor()
    mycursor.execute(_sql)
    _imgs_paths = np.array(mycursor.fetchall(), dtype=str)
    return _imgs_paths


def check_img_1(_path: str):
    _corrupt = False
    try:
        with open(_path, 'rb') as _f:
            _check_chars = _f.read()[-2:]
        if _check_chars != b'\xff\xd9':
            _corrupt = True
    except:
        _corrupt = True
    return _corrupt


def check_img_2(_path: str):
    _corrupt = False
    try:
        _img = Image.open(_path)
        _img.verify()
        _img.close()
        _img = Image.open(_path)
        _img.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        _img = np.array(_img, dtype=np.float32)
    except:
        _corrupt = True
    return _corrupt


def check_img_3(_path: str):

    def checkImage(fn):
        _proc = Popen(['identify', '-verbose', fn], stdout=PIPE, stderr=PIPE)
        _out, _err = _proc.communicate()
        _exitcode = _proc.returncode
        return _exitcode, _out, _err

    _corrupt = False
    try:
        _code, _output, _error = checkImage(_path)
        if str(_code) != '0' or str(_error, 'utf-8') != '':
            _corrupt = True
    except:
        _corrupt = True
    return _corrupt


def check_img(_path: str):
    _corrupt = False
    if check_img_1(_path):
        _corrupt = True
    elif check_img_2(_path):
        _corrupt = True
    elif check_img_3(_path):
        _corrupt = True
    return _corrupt


class VerifyFiles(object):

    def get_file(self, _img_path):

        _id_img = _img_path[0]
        _name = _img_path[1]
        _path = _img_path[2]
        _ext = os.path.splitext(_name)[1]
        _name_quote = str.replace(_name, _ext, '')

        _id_aux = np.where(imgs_paths[:, 0] == _img_path[0])[0][0]
        _progress = '[' + str(_id_aux + 1).rjust(imgs_paths_digits, '0') + '/' + str(imgs_paths_num) + '] - '

        _corrupt = (check_img(_path + _name) == True) + 0

        if _corrupt == 1:
            print(_progress + 'img corrupted: ' + _path + _name)

            _name_out = logs_dir + _name
            if os.path.isfile(_name_out):
                _name_out = logs_dir + _name_quote + '_' + _id_img + _ext
            copyfile(_path + _name, _name_out)

        else:
            print(_progress + 'img OK')

        _sql = ' update ' + table_aux_imgs + ' set ' \
               ' ' + field_check + ' = ' + str(_corrupt) + \
               ' where id_img = ' + str(_id_img) + ';'
        mydb.reconnect()
        mycursor = mydb.cursor()
        mycursor.execute(_sql)
        mydb.commit()

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
