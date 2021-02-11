
CREATE TABLE skus_imgs (
  id_img int(11) NOT NULL AUTO_INCREMENT,
  id_sku int(11) NOT NULL,
  id_num int(11) NOT NULL,
  url varchar(500) NOT NULL,
  name varchar(500) NOT NULL,
  path varchar(500) DEFAULT NULL,
  download varchar(100) DEFAULT NULL,
  check_1 int(1) DEFAULT NULL,
  check_2 int(1) DEFAULT NULL,
  check_3 int(1) DEFAULT NULL,
  hash varchar(1000) DEFAULT NULL,
  PRIMARY KEY (id_img,id_sku,id_num),
  KEY fk_products_images_1_idx (id_sku),
  CONSTRAINT fk_skus_images_1 FOREIGN KEY (id_sku) REFERENCES skus (id_sku) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
