### BundestagScraping
Project: Political Deception
Topic: Scraping the Bundestag website in order to get elected members information and social media accounts.


🔗 Data Source

All data is publicly available and scraped from the official Bundestag website:
https://www.bundestag.de/abgeordnete

## License

This project is licensed under the MIT License © 2025 Shahla Jahangiri.

# 🏛️ Bundestag Scraper

This project scrapes profile data for all current Bundestag members from the official website: [https://www.bundestag.de/abgeordnete](https://www.bundestag.de/abgeordnete).  
It captures names, party affiliation, biography details, committee memberships, and social media links.

---

## ⚙️ Chromedriver Setup

The code uses `webdriver-manager` to automatically handle the correct `chromedriver` version, so **manual download is not required**.

However, if you prefer to manage `chromedriver` yourself:
- Download it from: https://sites.google.com/chromium.org/driver/
- Place the executable in the **same directory** as your `.py` script.
- Ensure the version matches your installed version of Chrome.

---

## 📂 Files Overview

- `Bundestag.py`: Scrapes **all Bundestag members** (around 630 politicians).
- `Bundestag_Limited.py`: Scrapes a **limited number of members** (e.g. 5 or 100), based on the `MAX_MEMBERS` variable.
- `bundestag_profiles_all_complete.csv`: Output CSV with all scraped data (name, party, profile info, social media).

---

## 📝 Requirements

Install the required packages with:

```bash
pip install pandas bs4 selenium webdriver-manager lxml

