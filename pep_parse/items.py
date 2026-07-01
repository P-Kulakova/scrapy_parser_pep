"""Модели данных, которые формирует парсер PEP."""

import scrapy


class PepParseItem(scrapy.Item):
    """Данные одного документа PEP."""

    number = scrapy.Field()
    name = scrapy.Field()
    status = scrapy.Field()
