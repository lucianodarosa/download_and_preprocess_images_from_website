# DELETA AS IMAGENS DUPLICADAS SEGUINDO OS RESULTADOS DA BUSCA KNN

# ======================================
exit(0)
# ======================================

from libs import *

mydb = mysql_connect('database_v2')

table_skus_imgs = 'skus_imgs'

directory = '/home/lucianorosaserver/Desktop/nearest_skus_imgs_inuteis (copy)/'

imgs_paths = get_all_file_paths(directory, '.jpg')
imgs_paths.sort()
imgs_paths_num = len(imgs_paths)

if imgs_paths_num == 0:
    print('No files founded, aborted.')
    exit(0)

count_removed = 0
for img in imgs_paths:

    name = os.path.basename(img)
    id_img = int(name[0:9])

    sql = ' select path ' \
          ' from ' + table_skus_imgs + \
          ' where id_img = ' + str(id_img) + ';'
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    path = mycursor.fetchone()[0]

    try:

        os.remove(path + name)

        print(path + name)

        sql = ' update ' + table_skus_imgs + ' set ' \
              ' path=null, ' \
              ' download="Duplicate file", ' \
              ' check_1=null, ' \
              ' check_2=null, ' \
              ' hash=null ' \
              ' where id_img=' + str(id_img) + ';'
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()

        print('file removed: ' + path + name)

        count_removed += 1

    except:
        print('file already removed: ' + name)

print('\nimgs removed: ' + str(count_removed))

mydb.close()
