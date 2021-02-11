# ======================================
exit(0)
# ======================================

from libs import *

mydb = mysql_connect('database_v2')

directory = './logs_check_2/'
field_check = 'check_2'
table_skus_imgs = 'skus_imgs'

imgs_paths = get_all_file_paths(directory, '.jpg')
imgs_paths.sort()
imgs_paths_num = len(imgs_paths)

if imgs_paths_num == 0:
    print('No files founded, aborted.')
    exit(0)

sql = ' update ' + table_skus_imgs + ' set ' \
      ' ' + field_check + '=null;'
mycursor = mydb.cursor()
mycursor.execute(sql)
mydb.commit()

count_imgs = 0

print()
for img_path in imgs_paths:

    id_img = int(os.path.basename(img_path)[0:9])

    sql = ' update ' + table_skus_imgs + ' set ' \
          ' ' + field_check + '=1 '\
          ' where id_img = ' + str(id_img) + ';'
    mycursor.execute(sql)
    mydb.commit()

    print('[' + str(count_imgs + 1) + '/' + str(imgs_paths_num) + '] - img update: ' + img_path)

    count_imgs += 1

sql = ' update ' + table_skus_imgs + ' set '\
      ' ' + field_check + '=0 '\
      ' where download="Download file ok" '\
      ' and ' + field_check + ' is null;'
mycursor.execute(sql)
mydb.commit()

print('\nimgs updated: ' + str(count_imgs))

mydb.close()
