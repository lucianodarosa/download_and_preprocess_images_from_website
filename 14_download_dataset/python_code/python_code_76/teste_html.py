import html
import re


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, ' ', raw_html)
  return cleantext

aux = 'Top b&aacute;sico Blue Horse. Modelagem no estilo top fitness. Confeccionado em tecido homologado pela Invista, ' \
      'proporcionando qualidade, alta durabilidade e um caimento perfeito.<br />Composi&ccedil;&atilde;o: Light: 90% ' \
      'Poliamida e 10% Elastano.<br />Os nossos produtos n&atilde;o oferecem risco a sa&uacute;de e s&atilde;o ' \
      'totalmente seguro. Observe atentamente as orienta&ccedil;&otilde;es do modo de lavar dos produtos que constam ' \
      'no verso da etiqueta interna de composi&ccedil;&atilde;o.'

aux2 = '<p>&Uacute;til e descolado!&nbsp;O abridor de garrafa divertido possui revestimento de silicone colorido que ' \
       'facilita na hora do uso. Perfeito para quem curte dividir uma cervejinha com os amigos.</p><p>Material: ' \
       'Borracha pl&aacute;stica e metal.</p><p>Cuidados com o produto: Lavar com esponja macia, em &aacute;gua ' \
       'corrente e com detergente neutro.</p><p>Cor: Pink</p><div>MEDIDAS&nbsp;</div><div>Altura: 13&nbsp;cm<br />' \
       'Largura: 5&nbsp;cm</div>&nbsp;<p>&nbsp;</p><br />&nbsp;'

aux3 = cleanhtml(aux2)

print(html.unescape(aux3))
