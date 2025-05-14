import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)

driver.get("https://www.bundestag.de/abgeordnete")
time.sleep(2)

try:
    list_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "i.icon-list-bullet")))
    list_btn.click()
    time.sleep(3)
except:
    print("Already in list view or button not clickable.")

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
print("Finished scrolling, all members loaded.")

wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.bt-teaser-person")))

all_data = []
social_media_labels = set()
idx = 0

while True:
    tiles = driver.find_elements(By.CSS_SELECTOR, "div.bt-teaser-person")
    if idx >= len(tiles):
        break

    try:
        print(f" Visiting {idx+1}/{len(tiles)}")
        tile = tiles[idx]
        driver.execute_script("arguments[0].scrollIntoView(true);", tile)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", tile)
        time.sleep(2)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "lxml")

        def safe_select(selector):
            el = soup.select_one(selector)
            return el.get_text(strip=True) if el else None

        profile_url = driver.current_url

        full_name_raw = safe_select("h1.m-biography__introName") or ""

        if not full_name_raw or full_name_raw.strip().lower() == "symbolbild":
            full_name = ""
            title = ""
            first_name = ""
            last_name = ""
            print(f" Incomplete profile at index {idx+1} - still saving!")
        else:
            title_pattern = re.compile(r"^(Dr\.|Prof\. Dr\.|Prof\.)\s+", re.IGNORECASE)
            title_match = title_pattern.match(full_name_raw)
            if title_match:
                title = title_match.group(1).strip()
                full_name_clean = re.sub(title_pattern, "", full_name_raw).strip()
            else:
                title = ""
                full_name_clean = full_name_raw.strip()

            name_parts = full_name_clean.split()
            if len(name_parts) == 1:
                first_name = last_name = name_parts[0]
            else:
                first_name = " ".join(name_parts[:-1])
                last_name = name_parts[-1]

            full_name = full_name_clean

        party = profession = None
        info_block = soup.select_one("p.m-biography__introInfo")
        if info_block:
            span = info_block.select_one("span")
            strong = info_block.select_one("strong")
            if span:
                profession = span.get_text(strip=True)
            if strong:
                party = strong.get_text(strip=True)

        full_text = soup.get_text(separator="\n")
        birth = marital = None
        birth_match = re.search(r"geboren.*?in\s+([^\n\r<]+)", full_text, re.IGNORECASE)
        if birth_match:
            birth = birth_match.group(1).strip()
        if re.search(r"verheiratet", full_text, re.IGNORECASE):
            marital = "verheiratet"
        elif re.search(r"ledig", full_text, re.IGNORECASE):
            marital = "ledig"
        elif re.search(r"geschieden", full_text, re.IGNORECASE):
            marital = "geschieden"

        constituency = None
        state_el = soup.select_one("div.m-biography__constituencyInfo p strong")
        if state_el:
            constituency = state_el.get_text(strip=True)

        constituency_info = None
        label_el = soup.select_one("div.m-biography__constituencyInfo span.a-link__label")
        if label_el and "Wahlkreis" in label_el.text:
            constituency_info = label_el.get_text(strip=True)

        social_links = {}
        for link in soup.select("ul.e-linkList li a"):
            label = link.get("title", "").strip()
            href = link.get("href", "").strip()
            if label and href:
                social_links[label] = href
                social_media_labels.add(label)

        row = {
            "Title": title,
            "Full Name": full_name,
            "First Name": first_name,
            "Last Name": last_name,
            "Party": party,
            "Profession": profession,
            "Birthplace": birth,
            "Marital Status": marital,
            "Constituency": constituency,
            "Constituency Info": constituency_info,
            "Profile URL": profile_url
        }

        row.update(social_links)
        all_data.append(row)

        try:
            close = driver.find_element(By.CSS_SELECTOR, "a.bt-close-overlay")
            close.click()
            time.sleep(1)
        except:
            driver.back()
            time.sleep(2)

        idx += 1

    except Exception as e:
        print(f" Error on member {idx+1}: {e}")
        idx += 1
        continue

driver.quit()

df = pd.DataFrame(all_data)
df.drop_duplicates(subset=["Profile URL"], inplace=True)
df.insert(0, "No", range(1, len(df) + 1))

for label in sorted(social_media_labels):
    if label not in df.columns:
        df[label] = ""

df.to_csv("bundestag_profiles_all_complete.csv", index=False, encoding="utf-8-sig")
print("Finished, All members scraped with reliable names + social links + constituency info!")
