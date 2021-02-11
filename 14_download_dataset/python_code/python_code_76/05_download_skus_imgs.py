# FAZ O DOWNLOAD DAS IMAGENS UTILIZANDO AS RESPECTIVAS URLS

# ======================================
exit(0)
# ======================================

import urllib.request
from multiprocessing import Pool
import numpy as np
import time
from libs import *

mydb = mysql_connect('database_v1')

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36')]
req = urllib.request.install_opener(opener)

directory = '/media/lucianorosaserver/SSD_SATA_3/datasets/43_dataset/raw/images_v3/'
table_skus_imgs = 'skus_imgs'

pool_size = 6
batch_size = 1200
batch_digits = len(str(batch_size))


def find_skus_images_remaining():

    sql = ' select count(*) '\
          ' from ' + table_skus_imgs + \
          ' where download is null '\
          ' or (download <> %s '\
          ' and download <> %s);'
    values = ('%s' % "Download file ok", '%s' % "HTTP Error 404: Not Found")
    mydb.reconnect()
    mycursor = mydb.cursor()
    mycursor.execute(sql, values)
    remaining = mycursor.fetchone()
    return remaining[0]


def find_skus_images(batch):

    sql = ' select id_img, id_sku, id_num, url, name, download '\
          ' from ' + table_skus_imgs + \
          ' where download is null '\
          ' or (download <> %s '\
          ' and download <> %s) '\
          ' order by id_sku, id_img, id_num '\
          ' limit ' + str(batch) + ';'
    values = ('%s' % "Download file ok", '%s' % "HTTP Error 404: Not Found")
    mydb.reconnect()
    mycursor = mydb.cursor()
    mycursor.execute(sql, values)
    skus_images = np.array(mycursor.fetchall(), dtype=str)
    return skus_images


class DownloadFiles(object):

    def get_file(self, sku_image):

        time.sleep(0.100)  # 0.1 seconds

        try:
            urllib.request.urlretrieve(sku_image[3], directory + sku_image[4])
            msg = 'Download file ok'

        except FileNotFoundError as err:
            msg = str(err)

        except urllib.error.HTTPError as err:
            msg = str(err)

        except TimeoutError as err:
            msg = str(err)

        except Exception as err:
            msg = str(err)

        except TypeError as err:
            msg = str(err)

        except:
            msg = 'error download URL'

        id_sku_image = np.where(skus_images[:, 0] == sku_image[0])[0][0]

        sql = ' update ' + table_skus_imgs + ' set ' \
              ' download = "' + msg + '", ' \
              ' path = "' + directory + '" ' \
              ' where id_img = ' + sku_image[0] + ';'
        mydb.reconnect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()

        print('[' + str(id_sku_image + 1).rjust(batch_digits, '0') + '/' + str(batch_size) + '] - ' + msg)

    def download(self):

        pool = Pool(pool_size)
        pool.map(self.get_file, skus_images)
        pool.close()
        pool.join()


# ======================================
exit(0)
# ======================================

skus_images = find_skus_images(batch_size)

while len(skus_images) > 0:

    time.sleep(10)  # 10secs

    print('\n ======================== ini download batch\n')

    start_time_batch = time.time()

    d = DownloadFiles()
    d.download()

    end_time_batch = time.time() - start_time_batch

    days_batch, remainder = divmod(end_time_batch, 86400)
    hours_batch, remainder = divmod(remainder, 3600)
    minutes_batch, seconds_batch = divmod(remainder, 60)
    msg = '(%02dd:%02dh:%02dm:%02ds' % (days_batch, hours_batch, minutes_batch, seconds_batch) + ')'

    print('\n ======================== end download batch.: ' + msg)

    skus_images_remaining = find_skus_images_remaining()
    batches_remaining = get_shard_num(skus_images_remaining, batch_size)
    remaining_time = skus_images_remaining * end_time_batch

    print(' ======================== Remaining imgs.....: ' + str(skus_images_remaining))
    print(' ======================== Remaining batches..: ' + str(batches_remaining))

    skus_images = find_skus_images(batch_size)

mydb.close()
