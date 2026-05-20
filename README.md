### BundestagScraping
Project: Political Deception
Topic: Scraping the Bundestag website in order to get elected members information and social media accounts.


Data Source

All data is publicly available and scraped from the official Bundestag website:
https://www.bundestag.de/abgeordnete


# Bundestag Scraper

This project scrapes profile data for all current Bundestag members from the official website: [https://www.bundestag.de/abgeordnete](https://www.bundestag.de/abgeordnete).  
It captures names, party affiliation, biography details, committee memberships, and social media links.

---

## Chromedriver Setup

The code uses `webdriver-manager` to automatically handle the correct `chromedriver` version, so **manual download is not required**.

However, if you prefer to manage `chromedriver` yourself:
- Download it from: https://sites.google.com/chromium.org/driver/
- Place the executable in the **same directory** as your `.py` script.
- Ensure the version matches your installed version of Chrome.

---

## Files Overview

- `Bundestag.py`: Scrapes **all Bundestag members** (around 630 politicians).
- `Bundestag_Limited.py`: Scrapes a **limited number of members** (e.g. 5 or 100), based on the `MAX_MEMBERS` variable.
- `bundestag2025.csv`: Output CSV with all scraped data (name, party, profile info, social media).

---

## Requirements & Environment Setup

To keep dependencies clean and isolated, this project uses a Python virtual environment (`.venv`).

Follow these steps to create and activate your virtual environment:

1. Create the virtual environment:
```bash
python3 -m venv .venv
```
2. Activate the virtual environment:

    macOS/Linux: 
    ```bash
    source .venv/bin/activate
   ```
    
    Windows:
    ```bash
    .venv\Scripts\activate
   ```
    
### Install Required Packages

Once the virtual environment is activated, install all required Python packages with:

```bash
pip install pandas bs4 selenium webdriver-manager lxml



