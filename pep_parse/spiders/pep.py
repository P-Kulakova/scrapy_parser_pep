"""Паук для сбора документов PEP с сайта peps.python.org."""

import re
from urllib.parse import urlparse

import scrapy
from scrapy.http import TextResponse

from pep_parse.items import PepParseItem


PEP_PATH_PATTERN = re.compile(r'/pep-\d+/')
TITLE_SEPARATOR = ' – '


class PepSpider(scrapy.Spider):
    """Собирает номер, название и статус каждого документа PEP."""

    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response: TextResponse, **kwargs):
        """Создать запросы к страницам документов PEP."""
        for href in response.css('a::attr(href)').getall():
            pep_url = response.urljoin(href)
            pep_path = urlparse(pep_url).path

            if PEP_PATH_PATTERN.fullmatch(pep_path):
                yield response.follow(
                    pep_url,
                    callback=self.parse_pep,
                )

    def parse_pep(self, response: TextResponse) -> PepParseItem:
        """Извлечь номер, название и статус документа PEP."""
        title = ''.join(
            response.css('h1.page-title::text').getall()
        ).strip()

        pep_label, separator, name = title.partition(TITLE_SEPARATOR)

        if not separator:
            raise ValueError(f'Некорректный заголовок PEP: {title!r}')

        status_parts = response.xpath(
            '(//dt[contains(normalize-space(), "Status")]/'
            'following-sibling::dd[1])[1]'
            '//text()[normalize-space()]'
        ).getall()

        status = ' '.join(
            part.strip()
            for part in status_parts
        )

        return PepParseItem(
            number=pep_label.removeprefix('PEP ').strip(),
            name=name.strip(),
            status=status,
        )
