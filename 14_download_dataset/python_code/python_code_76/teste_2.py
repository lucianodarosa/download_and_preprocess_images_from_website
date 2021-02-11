# ======================================
#exit(0)
# ======================================

from libs import *

mydb = mysql_connect('database_v3')

#fields = ['product_name', 'cat_1', 'cat_2', 'cat_3', 'cat_4', 'cat_5', 'cat_6', 'main_category', 'sub_category', 'gender', 'google_product_category']
#fields = ['product_des']

# update lower all values
'''
_sql = ' update skus set ' \
       ' product_name = lower(product_name), ' \
       ' cat_1 = lower(cat_1), ' \
       ' cat_2 = lower(cat_2), ' \
       ' cat_3 = lower(cat_3), ' \
       ' cat_4 = lower(cat_4), ' \
       ' cat_5 = lower(cat_5), ' \
       ' cat_6 = lower(cat_6), ' \
       ' main_category = lower(main_category), ' \
       ' sub_category = lower(sub_category), ' \
       ' gender = lower(gender), ' \
       ' google_product_category = lower(google_product_category);'
'''

_sql = ' update skus set ' \
       ' product_description = lower(product_description);'
mycursor = mydb.cursor()
mycursor.execute(_sql)
mydb.commit()

'''
# update null none values
for field in fields:

    _sql = ' update skus set ' \
           + field + ' = null ' \
           ' where ' + field + ' = "none";'
    mycursor = mydb.cursor()
    mycursor.execute(_sql)
    mydb.commit()
'''
