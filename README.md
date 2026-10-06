# PEP Parser 🕷️

A Scrapy-based parser that collects information about Python Enhancement Proposals (PEPs) from the official Python PEP website.

The parser extracts the number, title, and current status of each PEP and generates CSV reports with the collected data and status statistics.

## Features

- Crawls the official Python PEP index
- Follows links to individual PEP pages
- Extracts PEP number, title, and status
- Exports collected data to CSV
- Calculates the number of PEPs for each status
- Generates a separate summary report
- Automatically adds timestamps to output filenames
- Includes automated tests with pytest

## Tech Stack

- Python
- Scrapy
- CSS selectors
- CSV
- pytest
- flake8

## Project Structure

```text
scrapy_parser_pep/
├── pep_parse/
│   ├── spiders/
│   │   └── pep.py        # PEP spider
│   ├── items.py          # Scraped data structure
│   ├── pipelines.py      # Status statistics and summary export
│   └── settings.py       # Scrapy configuration
├── results/              # Generated CSV reports
├── tests/                # Automated tests
├── requirements.txt
└── scrapy.cfg
```

## How It Works

The spider starts from the official PEP index and collects links to individual PEP documents.

For each PEP page, it extracts:

- PEP number
- Title
- Status

Scrapy's Feed Exporter saves the collected data to:

```text
results/pep_<timestamp>.csv
```

The custom pipeline counts PEPs by status and generates a second report:

```text
results/status_summary_<timestamp>.csv
```

The summary also contains the total number of processed PEP documents.

## Output Example

Main report:

```csv
number,name,status
1,PEP Purpose and Guidelines,Active
8,Style Guide for Python Code,Active
20,The Zen of Python,Active
```

Status summary:

```csv
Статус,Количество
Active,35
Draft,42
Final,315
Total,392
```

## Installation

Clone the repository:

```bash
git clone https://github.com/P-Kulakova/scrapy_parser_pep.git
cd scrapy_parser_pep
```

Create a virtual environment:

### Windows / Git Bash

```bash
py -3.10 -m venv venv
source venv/Scripts/activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

Run the spider from the project root:

```bash
scrapy crawl pep
```

After the spider finishes, two CSV files will be created in the `results/` directory.

## Testing

Run the automated tests:

```bash
pytest
```

## Author

**Polina Kulakova**

Python Backend Developer

GitHub: [P-Kulakova](https://github.com/P-Kulakova)
