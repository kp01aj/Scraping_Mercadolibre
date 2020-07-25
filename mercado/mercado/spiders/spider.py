import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from mercado.items import MercadoItem
from scrapy.exceptions import CloseSpider

class MercadoSpider(CrawlSpider):
    name = 'mercado'
    # Limitar numero de item a buscar
    item_cout = 0
    # Para limitarlo a este dominio
    allowed_domain = ['www.mercadolibre.com.mx']
    # Donde realizara la busqueda
    start_urls = ['https://listado.mercadolibre.com.mx/laptop#D[A:laptop]']

    #Reglas para el xpaths del boton siguientes.
    rule = {
        Rule(LinkExtractor(allow=(), restrict_xpaths = ('//li[@class="andes-pagination__button andes-pagination__button--next"]/a'))),
        Rule(LinkExtractor(allow=(), restrict_xpaths = ('//h2[@class="item__title list-view-item-title"]')),
                            # funcion parse_item que siempre debe tener este nombre.
                            callback = 'parse_item', follow = False)
    }

    def parse_item(self, reponse):
        # Importar la infomacion de los productos del modulo items.py como una lista.
        ml_item = MercadoItem()
        
        # Asignar para recolectar las informaciones.

        # Info del producto del URL mas arriba.
        ml_item['titulo'] = reponse.xpath('normalize-space(//*[@id="short-desc"]/div/header/h1/text())').extract()
        ml_item['folio'] = reponse.xpath('normalize-space(//span[@class="item-info__id-number"]/text())').extract()
        ml_item['precio'] = reponse.xpath('normalize-space(//*[@id="productInfo"]/fieldset[1]/span/span[2]/text())').extract()
        ml_item['condicion'] = reponse.xpath('normalize-space(//div[@class="item-conditions"]/text())').extract()
        # En este filtro se estuvo que colocar un "CONTAINS" para poder atrapar el metodo completo.
        #Esta linea
        ml_item['envio'] = reponse.xpath('normalize-space(//*[contains(@class, "shipping-method-title")])').extract()
        #Hasta aqui
        ml_item['ubicacion'] = reponse.xpath('normalize-space(//*[@id="root-app"]/div/div[1]/div[2]/div[1]/section[2]/div[1]/p[2])').extract()
        ml_item['opiniones'] = reponse.xpath('normalize-space(//span[@class="review-summary-average"]/text())').extract()
        ml_item['ventas_producto'] = reponse.xpath('normalize-space(//*[@id="short-desc"]/div/dl/div/text())').extract()

        # Informacion de la tienda o vendedor.
        ml_item['vendedor_url'] = reponse.xpath('normalize-space(//*[starts-with(@class, "reputation-view-more card-block-link")]/@href)').extract()
        ml_item['tipo_vendedor'] = reponse.xpath('normalize-space()').extract()
        ml_item['reputacion'] = reponse.xpath('normalize-space(//*[@id="root-app"]/div[2]/div[1]/div[2]/div[1]/section[2]/div[2]/p[1]/text())').extract()
        ml_item['ventas_vendedor'] = reponse.xpath('normalize-space(//*[@id="root-app"]/div[2]/div[1]/div[2]/div[1]/section[2]/div[4]/dl/dd[1]/strong/text())').extract()

        # filtro para no tener problema que le haga scraping a todo.
        self.item_cout += 1

        # Conteo.
        if self.item_cout > 20:
            raise CloseSpider('item_exceeded')
        # Lo siguiente para que haga el bucle hasta completar.
        # proceso de bucle
        yield ml_item