# ======================================
#exit(0)
# ======================================

from libs import *
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt

mydb = mysql_connect('database_v3')

directory = './updates'
table_skus_imgs = 'skus_imgs'

category_files = get_all_file_paths(directory, '.txt')
category_files.sort()
category_files = np.array(category_files, dtype=str)
category_files_num = len(category_files)
category_files_digits = len(str(category_files_num))

if category_files_num == 0:
    print('No files founded, aborted.')
    exit(0)

labels = []
values = []

len_max = 0
skus_imgs_count = 0

for category_file in category_files:

    file1 = open(category_file, 'r+')
    skus = file1.readlines()

    id_skus = []
    for sku in skus:
        if bool(sku and sku.strip()):

            id_sku = sku[:sku.find(',')]
            id_skus.append(id_sku)

            _sql = ' select count(*) ' + \
                   ' from ' + table_skus_imgs + \
                   ' where download = "Download file ok" ' \
                   ' and id_sku=' + str(id_sku) + ';'
            mycursor = mydb.cursor()
            mycursor.execute(_sql)
            skus_imgs_count += mycursor.fetchone()[0]

    file1.close()

    cat_name = os.path.basename(category_file)
    cat_name, _ = os.path.splitext(cat_name)

    values.append(len(id_skus))
    labels.append(cat_name)

    if len_max < len(cat_name):
        len_max = len(cat_name)

skus_count = 0
for i in range(len(labels)):
    print(labels[i].ljust(len_max + 5) + str(values[i]))
    skus_count += int(values[i])

print()
print('total skus: ' + str(skus_count))
print('total imgs: ' + str(skus_imgs_count))

#exit(0)

ticks = np.arange(len(labels))

'''
plt.bar(ticks, values, align='center', alpha=0.5)
plt.xticks(ticks, labels)
plt.ylabel('Samples per class')
plt.title('dataset Classes')
plt.show()
'''

plt.barh(ticks, values, align='center', alpha=0.5)
plt.yticks(ticks, labels)
plt.xlabel('Samples per class')
plt.title('dataset Classes')
plt.show()
