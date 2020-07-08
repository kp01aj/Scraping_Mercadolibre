# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface



###
# Este modulo lo descargue de la pagina de documentacion de SCRAPY y lo adapte a la necesidades.
##

import scrapy
from scrapy import signals
from scrapy.exporters import CsvItemExporter
import csv


class MercadoPipeline:
    def __init__(self):
        self.files = {}

    @classmethod
    def  from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline
    
    def spider_opened(self, spider):
        # nombre del archivo.
        file = open('%s_item.cvs' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        
        #Campos a exportar (Si no quiere un campo, solo se borra)
        self.exporter.fields_to_export = ['titulo', 'folio', 'precio', 'condicion', 'envio', 'ubicacion', 'opiniones',
                           'ventas_producto', 'vendedor_url', 'tipo_vendedor', 'reputacion', 'ventas_vendedor']
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item