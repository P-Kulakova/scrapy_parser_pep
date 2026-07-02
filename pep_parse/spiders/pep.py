"""Паук для сбора документов PEP с сайта peps.python.org."""

import scrapy
from scrapy.http import TextResponse

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    """Собирает номер, название и статус каждого документа PEP."""

    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response: TextResponse, **kwargs):
        """Создать запросы к страницам документов PEP."""
        for tr in response.css('section#numerical-index tbody tr'):
            pep_link = tr.css('a').attrib['href']
            yield response.follow(
                pep_link,
                callback=self.parse_pep,
            )

    def parse_pep(self, response: TextResponse) -> PepParseItem:
        """Извлечь номер, название и статус документа PEP."""
        table = response.css('dl.field-list')
        number = table.css('dt:contains("PEP") + dd::text').get()
        name = table.css('dt:contains("Title") + dd::text').get()
        status = table.css('dt:contains("Status") + dd::text').get()

        return PepParseItem(
            number=number,
            name=name,
            status=status,
        )
