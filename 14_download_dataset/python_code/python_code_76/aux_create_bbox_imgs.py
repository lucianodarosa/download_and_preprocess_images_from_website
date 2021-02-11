
# ======================================
exit(0)
# ======================================

from multiprocessing import Pool
import time
import numpy as np
import json
from PIL import Image
from shutil import copyfile
import os
import uuid

ext_imgs = '.jpg'

pool_size = 12

split_name = 'retrieval'

dir_origem = '/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/photos_2/'

dir_destino = '/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/photos_3/' + split_name + '/'

#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_bags.json', 'bags']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_belts.json', 'belts']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_dresses.json', 'dresses']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_eyewear.json', 'eyewear']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_footwear.json', 'footwear']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_hats.json', 'hats']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_leggings.json', 'leggings']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_outerwear.json', 'outerwear']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_pants.json', 'pants']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_skirts.json', 'skirts']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_tops.json', 'tops']

#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_bags.json', 'bags']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_belts.json', 'belts']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_dresses.json', 'dresses']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_eyewear.json', 'eyewear']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_footwear.json', 'footwear']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_hats.json', 'hats']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_leggings.json', 'leggings']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_outerwear.json', 'outerwear']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_pants.json', 'pants']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_skirts.json', 'skirts']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_tops.json', 'tops']

#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_bags.json', 'bags']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_belts.json', 'belts']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_dresses.json', 'dresses']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_eyewear.json', 'eyewear']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_footwear.json', 'footwear']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_hats.json', 'hats']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_leggings.json', 'leggings']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_outerwear.json', 'outerwear']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_pants.json', 'pants']
#json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_skirts.json', 'skirts']
json_dir = ['/media/lucianorosaserver/SSD_SATA_3/datasets/03_Street2shop/meta/meta/json/'+split_name+'_tops.json', 'tops']


def find_labels_retrieval(_json_dir):

    with open(_json_dir[0]) as json_file:
        data = json.load(json_file)

        _imgs_data = []
        for i, p in enumerate(data):

            name = str(p['photo']).rjust(9, '0')

            _imgs_data.append([name])

    _imgs_data = np.asarray(_imgs_data)
    return _imgs_data


def find_labels(_json_dir):

    with open(_json_dir[0]) as json_file:
        data = json.load(json_file)

        _imgs_data = []
        for i, p in enumerate(data):

            name = str(p['photo']).rjust(9, '0')

            width = str(int(p['bbox']['width'])).rjust(4, '0')
            top = str(int(p['bbox']['top'])).rjust(4, '0')
            height = str(int(p['bbox']['height'])).rjust(4, '0')
            left = str(int(p['bbox']['left'])).rjust(4, '0')

            _imgs_data.append([name, width, top, height, left])

    _imgs_data = np.asarray(_imgs_data)
    return _imgs_data


class VerifyFiles_retrieval(object):

    def get_file(self, _img_path):

        _id_aux = np.where(imgs_data[:, 0] == _img_path[0])[0][0]
        _progress = '[' + str(_id_aux + 1).rjust(imgs_data_digits, '0') + '/' + str(imgs_data_num) + '] - '

        name = str(_img_path[0])

        file_exists = True
        try:

            img1 = Image.open(dir_origem + name + ext_imgs)

        except:
            print(_progress + 'file not found - ' + name + ext_imgs)
            file_exists = False

        if file_exists:

            try:

                img2 = np.array(img1)
                img2 = Image.fromarray(img2).convert('RGB')

                id_unique = ''
                if os.path.isfile(dir_destino_cat + '/' + name + ext_imgs):
                    id_unique = '_' + str(uuid.uuid4())

                img2.save(dir_destino_cat + '/' + name + id_unique + ext_imgs)

                img1.close()
                img2.close()

                print(_progress + 'img OK')

            except:
                print(_progress + 'error copy - ' + name + ext_imgs)

    def Verify(self):

        pool = Pool(pool_size)
        pool.map(self.get_file, imgs_data)
        pool.close()
        pool.join()
        pool.terminate()
        del pool


class VerifyFiles(object):

    def get_file(self, _img_path):

        _id_aux = np.where(imgs_data[:, 0] == _img_path[0])[0][0]
        _progress = '[' + str(_id_aux + 1).rjust(imgs_data_digits, '0') + '/' + str(imgs_data_num) + '] - '

        name = str(_img_path[0])
        width_b = int(_img_path[1])
        top_b = int(_img_path[2])
        height_b = int(_img_path[3])
        left_b = int(_img_path[4])

        file_exists = True
        try:

            img1 = Image.open(dir_origem + name + ext_imgs)

        except:
            print(_progress + 'file not found - ' + name + ext_imgs)
            file_exists = False

        if file_exists:

            try:

                width, height = img1.size
                img2 = np.array(img1)
                img2 = img2[top_b:top_b + height_b, left_b:left_b + width_b]
                img2 = Image.fromarray(img2).convert('RGB')

                id_unique = ''
                if os.path.isfile(dir_destino_cat + '/' + name + ext_imgs):
                    id_unique = '_' + str(uuid.uuid4())

                img2.save(dir_destino_cat + '/' + name + id_unique + ext_imgs)

                img1.close()
                img2.close()

                print(_progress + 'img OK')

            except:

                print(_progress + 'error crop - ' + name + ext_imgs + ' - [' + str(width) + ', ' + str(height) + '] - [' + str(
                    width_b) + ', ' + str(top_b) + ', ' + str(height_b) + ', ' + str(left_b) + ']')
                copyfile(dir_origem + name + ext_imgs, dir_destino_cat_error + '/' + name + ext_imgs)

    def Verify(self):

        pool = Pool(pool_size)
        pool.map(self.get_file, imgs_data)
        pool.close()
        pool.join()
        pool.terminate()
        del pool


imgs_data = find_labels_retrieval(json_dir)
imgs_data_num = len(imgs_data)
imgs_data_digits = len(str(imgs_data_num))

np.savetxt(dir_destino + json_dir[1] + '.txt', imgs_data, fmt='%s')

dir_destino_cat = dir_destino + json_dir[1]
dir_destino_cat_error = dir_destino + json_dir[1] + '_crop_error'

try:
    os.mkdir(dir_destino_cat)
    os.mkdir(dir_destino_cat_error)
except:
    pass

print('\n ===================================== ini \n')

start_time_batch = time.time()

d = VerifyFiles_retrieval()
d.Verify()

end_time_batch = time.time() - start_time_batch

# calculate and show time
days_batch, remainder = divmod(end_time_batch, 86400)
hours_batch, remainder = divmod(remainder, 3600)
minutes_batch, seconds_batch = divmod(remainder, 60)
msg = '(%02dd:%02dh:%02dm:%02ds' % (days_batch, hours_batch, minutes_batch, seconds_batch) + ')'
print('\n ===================================== end: ' + msg)