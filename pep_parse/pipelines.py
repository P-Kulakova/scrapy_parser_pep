"""Обработка собранных PEP и формирование сводного CSV-файла."""

import csv
from collections import Counter
from datetime import datetime

from pep_parse.settings import BASE_DIR


RESULTS_DIR = 'results'
SUMMARY_FILENAME = 'status_summary_{time}.csv'
SUMMARY_HEADERS = ('Статус', 'Количество')
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
TOTAL_LABEL = 'Total'


class PepParsePipeline:
    """Подсчитывает документы по статусам и сохраняет сводку."""

    def open_spider(self, spider):
        """Создать счётчик статусов перед началом работы паука."""
        self.status_counts = Counter()

    def process_item(self, item, spider):
        """Учесть статус PEP и передать Item следующему обработчику."""
        self.status_counts[item['status']] += 1
        return item

    def close_spider(self, spider):
        """Сохранить сводку после завершения работы паука."""
        results_dir = BASE_DIR / RESULTS_DIR
        results_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime(DATETIME_FORMAT)
        filepath = results_dir / SUMMARY_FILENAME.format(time=timestamp)

        status_rows = sorted(self.status_counts.items())
        total = sum(self.status_counts.values())

        with filepath.open(
            mode='w',
            encoding='utf-8',
            newline='',
        ) as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(SUMMARY_HEADERS)
            writer.writerows(status_rows)
            writer.writerow((TOTAL_LABEL, total))
