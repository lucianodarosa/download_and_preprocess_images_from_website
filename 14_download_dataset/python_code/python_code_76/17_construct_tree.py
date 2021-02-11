# CONSTRÓI E SALVA A ÁRVORE DE BUSCA (KNN) UTILIZANDO OS CÓDIGOS HASH GERADOS

# ======================================
exit(0)
# ======================================

import time
import numpy as np
from sklearn.neighbors import BallTree
import joblib
from libs import *

mydb = mysql_connect('database_v2')

table_skus_imgs = 'skus_imgs'


def find_skus_imgs():

    _sql = ' select id_img, path, name, hash '\
           ' from ' + table_skus_imgs + \
           ' where download = "Download file ok" '\
           ' and hash is not null;'
    mycursor = mydb.cursor()
    mycursor.execute(_sql)
    _skus_images = np.array(mycursor.fetchall(), dtype=np.str)
    return _skus_images


skus_imgs = find_skus_imgs()

hashes = []
for sku_img in skus_imgs:
    hashes.append([int(x) for s in sku_img[3] for x in s])
hashes = np.asarray(hashes, dtype=np.int)

print('\n ===================================== ini construct tree\n')

start_time_batch = time.time()

tree = BallTree(hashes, leaf_size=40, metric='hamming')
joblib.dump(tree, './tree/BallTree.joblib')

end_time_batch = time.time() - start_time_batch

# calculate and show time
days_batch, remainder = divmod(end_time_batch, 86400)
hours_batch, remainder = divmod(remainder, 3600)
minutes_batch, seconds_batch = divmod(remainder, 60)
msg = '(%02dd:%02dh:%02dm:%02ds' % (days_batch, hours_batch, minutes_batch, seconds_batch) + ')'
print('\n ===================================== end construct tree: ' + msg)

mydb.close()
