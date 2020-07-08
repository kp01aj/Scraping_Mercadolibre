# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MercadoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

"""
Sacando informacion de la pagina de Mercado Libre

Esta URL de busqueda.
    https://listado.mercadolibre.com.mx/impresion#[A:impresoras]
    https://listado.mercadolibre.com.mx/celulares#D[A:celulares]
    https://listado.mercadolibre.com.mx/laptop#D[A:laptop]


Vendedor
    https://www.mercadolibre.com.mx/impresora-xerox-phaser-3020bi-con-wifi-110v-127v-blanca-y-azul/p/MLM7975191/seller-info

"""

class MercadoItem(scrapy.Item):
    # Info del producto del URL mas arriba.
    titulo = scrapy.Field()
    folio = scrapy.Field()
    precio = scrapy.Field()
    condicion = scrapy.Field()
    envio = scrapy.Field()
    ubicacion = scrapy.Field()
    opiniones = scrapy.Field()
    ventas_producto = scrapy.Field()

    # Informacion de la tienda o vendedor.
    vendedor_url = scrapy.Field()
    tipo_vendedor = scrapy.Field()
    reputacion = scrapy.Field()
    ventas_vendedor = scrapy.Field()