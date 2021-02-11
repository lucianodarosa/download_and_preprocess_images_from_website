# EXECUTA A BUSCA PELOS VIZINHOS MAIS PRÓXIMOS
# RECUPERA VIZINHOS COM ÍNDICE DE SEMELHANÇA <= 0.1
# SALVA A QUERY E OS RESULTADOS EM UMA PASTA PARA CONFERÊNCIA

# ======================================
#exit(0)
# ======================================

from multiprocessing import Pool
import time
import numpy as np
import shutil
import joblib
from libs import *

mydb = mysql_connect('database_v2')

path_out = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/tree_nearest_skus_imgs'
path_tree = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/files/logs/tree/BallTree.joblib'
table_skus_imgs = 'skus_imgs'
pool_size = 12


def find_skus_imgs():

    _sql = ' select id_img, path, name, hash '\
           ' from ' + table_skus_imgs + \
           ' where download = "Download file ok" '\
           ' and hash is not null;'
    mycursor = mydb.cursor()
    mycursor.execute(_sql)
    _skus_images = np.array(mycursor.fetchall(), dtype=np.str)
    return _skus_images


class VerifyFiles(object):

    def get_file(self, _sku_img):

        _id_img = _sku_img[0]
        _path = _sku_img[1]
        _name = _sku_img[2]
        _hash = _sku_img[3]

        _id_aux = bin_search(skus_imgs_ids, int(_id_img), 0, len(skus_imgs) - 1)

        _progress = '[' + str(_id_aux + 1).rjust(skus_imgs_digits, '0') + '/' + str(skus_imgs_num) + '] - '

        ids_results = tree.query_radius(hashes[_id_aux:_id_aux + 1], r=0.1)[0]

        if len(ids_results) > 1:

            mydb.reconnect()
            mycursor_insert = mydb.cursor()

            _valids = []
            for id in ids_results:

                if _id_img == skus_imgs[id][0]:
                    continue

                _sql = ' select count(*) ' \
                       ' from combinations ' \
                       ' where id_1=' + skus_imgs[id][0] + \
                       ' and id_2=' + _id_img + ';'
                mycursor = mydb.cursor()
                mycursor.execute(_sql)
                result_sql = mycursor.fetchone()[0]
                mycursor.close()

                if result_sql == 0:

                    _sql = ' insert into combinations ' \
                           ' (id_1, id_2) ' \
                           ' values (%s, %s);'
                    _values = ('%s' % _id_img,
                               '%s' % skus_imgs[id][0])
                    mycursor_insert.execute(_sql, _values)

                    _valids.append([skus_imgs[id][1], skus_imgs[id][2]])

            if len(_valids) != 0:

                mydb.commit()

                print(_progress + str(len(_valids)))

                #'''
                new_folder_name = _name[:-4]
                os.mkdir(path_out + slash + new_folder_name)

                shutil.copy(_path + slash + _name, path_out + slash + new_folder_name + slash + _name)

                for j in range(len(_valids)):
                    shutil.copy(_valids[j][0] + slash + _valids[j][1], path_out + slash + new_folder_name + slash + _valids[j][1])
                #'''

    def Verify(self):

        #id_ini = 0
        #id_end = 100000

        #id_ini = 100000
        #id_end = 200000

        #id_ini = 200000
        #id_end = 300000

        #id_ini = 300000
        #id_end = 400000

        #id_ini = 400000
        #id_end = 500000

        #id_ini = 500000
        #id_end = 600000

        #id_ini = 600000
        #id_end = 700000

        id_ini = 700000

        pool = Pool(pool_size)
        #pool.map(self.get_file, skus_imgs[id_ini:id_end])
        pool.map(self.get_file, skus_imgs[id_ini:])
        pool.close()
        pool.join()
        pool.terminate()
        del pool


skus_imgs = find_skus_imgs()
skus_imgs_num = len(skus_imgs)
skus_imgs_digits = len(str(skus_imgs_num))

skus_imgs_ids = np.array(skus_imgs[:, 0], dtype=np.int)

hashes = []
for sku_img in skus_imgs:
    hashes.append([int(x) for s in sku_img[3] for x in s])
hashes = np.asarray(hashes, dtype=np.int)

tree = joblib.load(path_tree)

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
