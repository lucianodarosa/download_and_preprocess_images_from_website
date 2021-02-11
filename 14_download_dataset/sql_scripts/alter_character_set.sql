
# option 1
#ALTER TABLE your_database_name.your_table CONVERT TO CHARACTER SET utf8;

# option 2
#ALTER TABLE your_db_name.table_name MODIFY COLUMN column_name text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;

ALTER TABLE skus2 MODIFY COLUMN product_description text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;
