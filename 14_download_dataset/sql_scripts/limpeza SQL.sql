

deletar todos os produtos que não possuirem imagens baixadas

select k.id_sku, COUNT(k.id_sku)
from skus k
inner join skus_images i
on k.id_sku = i.id_sku
and i.status_download <> 'Download file ok'
GROUP BY k.id_sku
HAVING COUNT(k.id_sku) = 6




