select distinct(cat_1), count(cat_1) total_cat
from skus
where cat_1 is not null
and skus.id_sku in (select id_sku
					  from skus_images 
					  where skus_images.id_sku = skus.id_sku 
					  and status_download = 'Download file ok' )
group by cat_1
order by cat_1 asc


select distinct(cat_2), count(cat_2) total_cat
from skus
where cat_2 is not null
and skus.id_sku in (select id_sku
					  from skus_images 
					  where skus_images.id_sku = skus.id_sku 
					  and status_download = 'Download file ok' )
group by cat_2
order by cat_2 asc


select distinct(cat_3), count(cat_3) total_cat
from skus
where cat_3 is not null
and skus.id_sku in (select id_sku
					  from skus_images 
					  where skus_images.id_sku = skus.id_sku 
					  and status_download = 'Download file ok' )
group by cat_3
order by cat_3 asc


select distinct(cat_4), count(cat_4) total_cat
from skus
where cat_4 is not null
and skus.id_sku in (select id_sku
					  from skus_images 
					  where skus_images.id_sku = skus.id_sku 
					  and status_download = 'Download file ok' )
group by cat_4
order by cat_4 asc


select distinct(cat_5), count(cat_5) total_cat
from skus
where cat_5 is not null
and skus.id_sku in (select id_sku
					  from skus_images 
					  where skus_images.id_sku = skus.id_sku 
					  and status_download = 'Download file ok' )
group by cat_5
order by cat_5 asc


select distinct(cat_6), count(cat_6) total_cat
from skus
where cat_6 is not null
and skus.id_sku in (select id_sku
					  from skus_images 
					  where skus_images.id_sku = skus.id_sku 
					  and status_download = 'Download file ok' )
group by cat_6
order by cat_6 asc


select distinct(main_category), count(main_category) total_cat
from skus
where main_category is not null
and skus.id_sku in (select id_sku
					  from skus_images 
					  where skus_images.id_sku = skus.id_sku 
					  and status_download = 'Download file ok' )
group by main_category
order by main_category asc


select distinct(gender), count(gender) total_cat
from skus
where gender is not null
and skus.id_sku in (select id_sku
					  from skus_images 
					  where skus_images.id_sku = skus.id_sku 
					  and status_download = 'Download file ok' )
group by gender
order by gender asc






