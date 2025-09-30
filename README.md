# House Finder Bot

Automates house hunting by scraping property listings and filling Google Forms.

## Setup

1. Install dependencies: ```bash
pip install -r requirements.txt```

2. Run the bot: ```bash
python main.py```

3. Enter URLs when prompted:
   - Google Form link
   - Website to scrape

## What it does

1. **Scrapes** property listings from websites
2. **Parses** address, price, and links
3. **Fills** Google Forms automatically

## Files

- `main.py` - Main orchestrator
- `house_scrape.py` - Web scraping
- `house_parser.py` - HTML parsing
- `data_filler.py` - Form automation
- `models.py` - Data structures

## Requirements

- Python 3.8+
- Chrome browser
- Internet connection
